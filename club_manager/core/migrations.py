# -*- coding: utf-8 -*-
"""
Système de migrations du schéma SQLite de Club Manager.

La version du schéma est stockée dans ``PRAGMA user_version``. Chaque migration
est une fonction ``(connection) -> None`` appliquée dans l'ordre des versions.

Migrations existantes :
    1. Ajout des champs de paiement (cash_amount, check1..3_amount, total_paid)
    2. Ajout de birth_date et other_mjc_clubs
    3. Suppression des colonnes obsolètes health et external_club
"""

import sqlite3
from typing import Callable, Dict, List

from club_manager.core.logger import get_logger

logger = get_logger(__name__)

Migration = Callable[[sqlite3.Connection], None]

MEMBERS_COLUMNS = [
    "id",
    "last_name",
    "first_name",
    "address",
    "postal_code",
    "city",
    "phone",
    "mail",
    "rgpd",
    "image_rights",
    "payment_type",
    "ancv_amount",
    "cash_amount",
    "check1_amount",
    "check2_amount",
    "check3_amount",
    "total_paid",
    "mjc_club_id",
    "cotisation_status",
    "birth_date",
    "other_mjc_clubs",
]


def _members_columns(conn: sqlite3.Connection) -> List[str]:
    return [row[1] for row in conn.execute("PRAGMA table_info(members)").fetchall()]


def _add_columns(conn: sqlite3.Connection, columns: Dict[str, str]) -> None:
    existing = _members_columns(conn)
    for name, definition in columns.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE members ADD COLUMN {name} {definition}")


def _migration_1_payment_fields(conn: sqlite3.Connection) -> None:
    """Ajoute les champs de paiement."""
    _add_columns(
        conn,
        {
            "cash_amount": "REAL DEFAULT 0",
            "check1_amount": "REAL DEFAULT 0",
            "check2_amount": "REAL DEFAULT 0",
            "check3_amount": "REAL DEFAULT 0",
            "total_paid": "REAL DEFAULT 0",
        },
    )


def _migration_2_birth_and_clubs(conn: sqlite3.Connection) -> None:
    """Ajoute birth_date et other_mjc_clubs."""
    _add_columns(conn, {"birth_date": "TEXT", "other_mjc_clubs": "TEXT"})


def _migration_3_drop_obsolete(conn: sqlite3.Connection) -> None:
    """Supprime health et external_club (reconstruction de table)."""
    columns = _members_columns(conn)
    if "health" not in columns and "external_club" not in columns:
        return
    to_copy = [c for c in columns if c in MEMBERS_COLUMNS]
    conn.execute("""
        CREATE TABLE members_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT, first_name TEXT, address TEXT, postal_code TEXT, city TEXT,
            phone TEXT, mail TEXT, rgpd INTEGER, image_rights INTEGER,
            payment_type TEXT,
            ancv_amount REAL,
            cash_amount REAL DEFAULT 0,
            check1_amount REAL DEFAULT 0,
            check2_amount REAL DEFAULT 0,
            check3_amount REAL DEFAULT 0,
            total_paid REAL DEFAULT 0,
            mjc_club_id INTEGER,
            cotisation_status TEXT,
            birth_date TEXT,
            other_mjc_clubs TEXT,
            FOREIGN KEY(mjc_club_id) REFERENCES mjc_clubs(id)
        )
    """)
    cols = ", ".join(to_copy)
    conn.execute(f"INSERT INTO members_new ({cols}) SELECT {cols} FROM members")
    conn.execute("DROP TABLE members")
    conn.execute("ALTER TABLE members_new RENAME TO members")


MIGRATIONS: Dict[int, Migration] = {
    1: _migration_1_payment_fields,
    2: _migration_2_birth_and_clubs,
    3: _migration_3_drop_obsolete,
}


class MigrationManager:
    """Gère les versions du schéma d'une base SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Args:
            connection: Connexion SQLite à migrer.
        """
        self.connection = connection

    @property
    def latest_version(self) -> int:
        """Dernière version de schéma connue."""
        return max(MIGRATIONS) if MIGRATIONS else 0

    def current_version(self) -> int:
        """Retourne la version courante du schéma (PRAGMA user_version)."""
        return int(self.connection.execute("PRAGMA user_version").fetchone()[0])

    def _members_table_exists(self) -> bool:
        row = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'").fetchone()
        return row is not None

    def migrate(self) -> int:
        """Applique les migrations en attente.

        Returns:
            Le nombre de migrations appliquées.
        """
        if not self._members_table_exists():
            return 0
        applied = 0
        for version in sorted(MIGRATIONS):
            if version <= self.current_version():
                continue
            logger.info("Application de la migration %d", version)
            try:
                MIGRATIONS[version](self.connection)
                self.connection.execute(f"PRAGMA user_version = {int(version)}")
                self.connection.commit()
            except sqlite3.Error:
                self.connection.rollback()
                logger.exception("Échec de la migration %d", version)
                raise
            applied += 1
        return applied
