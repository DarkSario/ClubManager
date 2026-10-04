# -*- coding: utf-8 -*-
"""Tests de l'atomicité des migrations."""

import logging
import sqlite3

import pytest

from club_manager.core import migrations
from club_manager.core.migrations import MigrationManager

OLD_SCHEMA = """
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT, first_name TEXT, health TEXT, external_club TEXT, mail TEXT
    )
"""


def _old_db(path, version=0):
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute(OLD_SCHEMA)
    conn.execute(
        "INSERT INTO members (last_name, first_name, health, external_club, mail) VALUES (?,?,?,?,?)",
        ("Dupont", "Jean", "RAS", "Autre", "j@d.fr"),
    )
    conn.execute(f"PRAGMA user_version = {version}")
    conn.commit()
    return conn


def _columns(conn):
    return [r[1] for r in conn.execute("PRAGMA table_info(members)")]


def _tables(conn):
    return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def test_migration_success_keeps_data(tmp_path):
    conn = _old_db(tmp_path / "old.db")
    manager = MigrationManager(conn)
    assert manager.migrate() == manager.latest_version
    cols = _columns(conn)
    assert "health" not in cols and "external_club" not in cols
    assert {"cash_amount", "birth_date", "other_mjc_clubs"} <= set(cols)
    row = conn.execute("SELECT * FROM members").fetchone()
    assert (row["last_name"], row["first_name"], row["mail"]) == ("Dupont", "Jean", "j@d.fr")
    assert manager.current_version() == manager.latest_version
    assert conn.isolation_level == ""
    assert not conn.in_transaction


def test_migration_is_idempotent(tmp_path):
    conn = _old_db(tmp_path / "old.db")
    manager = MigrationManager(conn)
    manager.migrate()
    snapshot = (_columns(conn), [tuple(r) for r in conn.execute("SELECT * FROM members")])
    assert manager.migrate() == 0
    assert (_columns(conn), [tuple(r) for r in conn.execute("SELECT * FROM members")]) == snapshot
    assert manager.current_version() == manager.latest_version


def test_no_members_table_is_noop(tmp_path):
    conn = sqlite3.connect(str(tmp_path / "empty.db"))
    assert MigrationManager(conn).migrate() == 0


def test_failing_migration_3_rolls_back(tmp_path, monkeypatch, caplog):
    conn = _old_db(tmp_path / "old.db", version=2)
    before_cols = _columns(conn)

    def failing(connection):
        migrations._migration_3_drop_obsolete(connection)
        raise RuntimeError("boom après DDL")

    monkeypatch.setitem(migrations.MIGRATIONS, 3, failing)
    manager = MigrationManager(conn)
    logging.getLogger("clubmanager").propagate = True
    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError):
            manager.migrate()
    assert _columns(conn) == before_cols
    assert "members_new" not in _tables(conn)
    assert manager.current_version() == 2
    assert conn.execute("SELECT COUNT(*) FROM members").fetchone()[0] == 1
    assert "Échec de la migration 3" in caplog.text
    assert conn.isolation_level == ""
    assert not conn.in_transaction


def test_failure_midway_after_ddl_keeps_earlier_versions(tmp_path, monkeypatch):
    conn = _old_db(tmp_path / "old.db", version=0)

    def failing(connection):
        connection.execute("CREATE TABLE leftover (x INTEGER)")
        raise sqlite3.OperationalError("échec")

    monkeypatch.setitem(migrations.MIGRATIONS, 3, failing)
    manager = MigrationManager(conn)
    with pytest.raises(sqlite3.OperationalError):
        manager.migrate()
    # Les migrations 1 et 2 ont été validées, la 3 annulée entièrement
    assert manager.current_version() == 2
    assert "leftover" not in _tables(conn)
    assert "health" in _columns(conn)
