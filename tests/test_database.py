# -*- coding: utf-8 -*-
"""Tests du module Database et des migrations."""

import sqlite3

from club_manager.core.database import Database
from club_manager.core.migrations import MigrationManager


def test_schema_created(db):
    tables = {r["name"] for r in db.query("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"members", "positions", "sessions", "cotisations", "settings", "mailing_logs"} <= tables


def test_execute_and_query(db):
    db.execute("INSERT INTO members (last_name) VALUES (?)", ["Dupont"])
    rows = db.query("SELECT last_name FROM members")
    assert rows[0]["last_name"] == "Dupont"


def test_singleton_and_change(tmp_path, db):
    assert Database.instance() is db
    other = Database.change_database(str(tmp_path / "other.db"))
    assert other is not db
    assert Database.instance(str(tmp_path / "other.db")) is other


def test_instance_with_new_path_switches(tmp_path, db):
    new = Database.instance(str(tmp_path / "third.db"))
    assert new.db_path.endswith("third.db")


def test_default_instance_after_close(tmp_path, monkeypatch):
    monkeypatch.setenv("CLUBMANAGER_DB_PATH", str(tmp_path / "default.db"))
    Database._instance = None
    Database._current_db_path = None
    inst = Database.instance()
    assert inst.db_path.endswith("default.db")
    inst.close()
    assert Database._instance is None


def test_schema_version_set(db):
    manager = MigrationManager(db.connection)
    assert manager.current_version() == manager.latest_version


def test_migration_from_legacy_schema(tmp_path):
    path = str(tmp_path / "legacy.db")
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE members (id INTEGER PRIMARY KEY AUTOINCREMENT, last_name TEXT, "
        "first_name TEXT, health TEXT, external_club TEXT)"
    )
    conn.execute("INSERT INTO members (last_name, first_name, health) VALUES ('A', 'B', 'x')")
    conn.commit()
    conn.close()

    database = Database(path)
    try:
        cols = [r[1] for r in database.connection.execute("PRAGMA table_info(members)")]
        assert "health" not in cols and "external_club" not in cols
        assert {"cash_amount", "birth_date", "other_mjc_clubs", "total_paid"} <= set(cols)
        assert database.query("SELECT last_name FROM members")[0]["last_name"] == "A"
        assert MigrationManager(database.connection).migrate() == 0
    finally:
        database.connection.close()


def test_migrate_without_members_table():
    conn = sqlite3.connect(":memory:")
    assert MigrationManager(conn).migrate() == 0
