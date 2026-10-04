# -*- coding: utf-8 -*-
"""
Module central d'accès et gestion à la base SQLite du Club Manager.
Responsable de l'initialisation, connexion, requêtes, migrations et transactions.
"""

import sqlite3
import threading
from typing import Any, List, Optional, Sequence

from club_manager.config import Config
from club_manager.core.logger import get_logger
from club_manager.core.migrations import MigrationManager

logger = get_logger(__name__)


class Database:
    """Accès singleton (thread-safe) à la base SQLite active."""

    _instance: Optional["Database"] = None
    _lock = threading.Lock()
    _current_db_path: Optional[str] = None

    @staticmethod
    def instance(db_path: Optional[str] = None) -> "Database":
        """Retourne l'instance unique, en changeant de base si ``db_path`` diffère.

        Args:
            db_path: Chemin de la base (défaut : ``Config.default_db_path()``).
        """
        with Database._lock:
            # Si un path est fourni et qu'il est différent, changer la base
            if db_path and Database._current_db_path != db_path:
                if Database._instance is not None:
                    Database._instance.connection.close()
                Database._instance = Database(db_path)
                Database._current_db_path = db_path
            # Si aucun path n'est fourni et qu'il n'y a pas d'instance, utiliser le défaut
            elif Database._instance is None:
                default_path = Config.default_db_path()
                Database._instance = Database(default_path)
                Database._current_db_path = default_path
            return Database._instance

    @staticmethod
    def change_database(db_path: str) -> "Database":
        """Change la base de données active."""
        with Database._lock:
            if Database._instance is not None:
                Database._instance.connection.close()
            Database._instance = Database(db_path)
            Database._current_db_path = db_path
            return Database._instance

    def __init__(self, db_path: str) -> None:
        """Ouvre la connexion et initialise le schéma.

        Args:
            db_path: Chemin du fichier SQLite.
        """
        logger.info("Ouverture de la base %s", db_path)
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.setup_schema()

    def setup_schema(self) -> None:
        """Crée les tables manquantes puis applique les migrations."""
        cursor = self.connection.cursor()
        # Extrait simplifié, à compléter/migrer selon les évolutions métiers
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS members (
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
            );
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, type TEXT, description TEXT, assigned_to INTEGER REFERENCES members(id)
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, start DATE, end DATE, club_amount REAL, mjc_amount REAL, is_current INTEGER
            );
            CREATE TABLE IF NOT EXISTS cotisations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER, session_id INTEGER, amount REAL, paid REAL, payment_date DATE,
                method TEXT, status TEXT, cheque_number TEXT,
                FOREIGN KEY(member_id) REFERENCES members(id),
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            );
            CREATE TABLE IF NOT EXISTS custom_fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, type TEXT, default_value TEXT, options TEXT, constraints TEXT
            );
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT, action TEXT, user TEXT, object TEXT, details TEXT
            );
            CREATE TABLE IF NOT EXISTS mjc_clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_date TEXT
            );
            CREATE TABLE IF NOT EXISTS annual_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT UNIQUE NOT NULL,
                club_price REAL NOT NULL,
                mjc_price REAL NOT NULL,
                is_current INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS mailing_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER,
                recipient_email TEXT,
                subject TEXT,
                status TEXT,
                message_id TEXT,
                error TEXT,
                timestamp TEXT,
                FOREIGN KEY(recipient_id) REFERENCES members(id)
            );
        """)
        self.connection.commit()
        self.migrate_schema()

    def migrate_schema(self) -> None:
        """Migre le schéma de base de données pour les bases existantes."""
        MigrationManager(self.connection).migrate()

    def execute(self, sql: str, params: Optional[Sequence[Any]] = None) -> sqlite3.Cursor:
        """Exécute une requête d'écriture et valide la transaction.

        Args:
            sql: Requête SQL.
            params: Paramètres de la requête.

        Returns:
            Le curseur résultant.
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, params or [])
        self.connection.commit()
        return cursor

    def query(self, sql: str, params: Optional[Sequence[Any]] = None) -> List[sqlite3.Row]:
        """Exécute une requête de lecture.

        Args:
            sql: Requête SQL.
            params: Paramètres de la requête.

        Returns:
            La liste des lignes.
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()

    def close(self) -> None:
        """Ferme la connexion et réinitialise le singleton."""
        logger.info("Fermeture de la base %s", self.db_path)
        self.connection.close()
        Database._instance = None
        Database._current_db_path = None
