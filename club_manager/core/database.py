# -*- coding: utf-8 -*-
"""
Module central d'accès et gestion à la base SQLite du Club Manager.
Responsable de l'initialisation, connexion, requêtes, migrations et transactions.
"""
import sqlite3
import threading

class Database:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def instance(db_path="club_manager.db"):
        with Database._lock:
            if Database._instance is None:
                Database._instance = Database(db_path)
            return Database._instance

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.setup_schema()

    def setup_schema(self):
        cursor = self.connection.cursor()
        # Extrait simplifié, à compléter/migrer selon les évolutions métiers
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT, first_name TEXT, address TEXT, postal_code TEXT, city TEXT,
                phone TEXT, mail TEXT, rgpd INTEGER, image_rights INTEGER,
                health TEXT, ancv INTEGER, cash REAL, cheque1 TEXT, cheque2 TEXT, cheque3 TEXT,
                total_paid REAL, club_part REAL, mjc_part REAL,
                external_club TEXT, mjc_elsewhere TEXT
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
                method TEXT, status TEXT,
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
        """)
        self.connection.commit()

    def execute(self, sql, params=None):
        cursor = self.connection.cursor()
        cursor.execute(sql, params or [])
        self.connection.commit()
        return cursor

    def query(self, sql, params=None):
        cursor = self.connection.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()

    def close(self):
        self.connection.close()
        Database._instance = None