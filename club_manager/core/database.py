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
    _current_db_path = None

    @staticmethod
    def instance(db_path=None):
        with Database._lock:
            # Si un path est fourni et qu'il est différent, changer la base
            if db_path and Database._current_db_path != db_path:
                if Database._instance is not None:
                    Database._instance.connection.close()
                Database._instance = Database(db_path)
                Database._current_db_path = db_path
            # Si aucun path n'est fourni et qu'il n'y a pas d'instance, utiliser le défaut
            elif Database._instance is None:
                default_path = "club_manager.db"
                Database._instance = Database(default_path)
                Database._current_db_path = default_path
            return Database._instance
    
    @staticmethod
    def change_database(db_path):
        """Change la base de données active."""
        with Database._lock:
            if Database._instance is not None:
                Database._instance.connection.close()
            Database._instance = Database(db_path)
            Database._current_db_path = db_path
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
                payment_type TEXT,
                ancv_amount REAL,
                cash_amount REAL DEFAULT 0,
                check1_amount REAL DEFAULT 0,
                check2_amount REAL DEFAULT 0,
                check3_amount REAL DEFAULT 0,
                total_paid REAL DEFAULT 0,
                mjc_club_id INTEGER,
                cotisation_status TEXT,
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
        """)
        self.connection.commit()
        self.migrate_schema()

    def migrate_schema(self):
        """Migre le schéma de base de données pour les bases existantes."""
        cursor = self.connection.cursor()
        
        # Vérifier si la table members existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'")
        if not cursor.fetchone():
            return  # Table n'existe pas encore, pas de migration nécessaire
        
        # Obtenir les colonnes actuelles de la table members
        cursor.execute("PRAGMA table_info(members)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Ajouter les nouveaux champs de paiement s'ils n'existent pas
        if 'cash_amount' not in columns:
            cursor.execute("ALTER TABLE members ADD COLUMN cash_amount REAL DEFAULT 0")
        if 'check1_amount' not in columns:
            cursor.execute("ALTER TABLE members ADD COLUMN check1_amount REAL DEFAULT 0")
        if 'check2_amount' not in columns:
            cursor.execute("ALTER TABLE members ADD COLUMN check2_amount REAL DEFAULT 0")
        if 'check3_amount' not in columns:
            cursor.execute("ALTER TABLE members ADD COLUMN check3_amount REAL DEFAULT 0")
        if 'total_paid' not in columns:
            cursor.execute("ALTER TABLE members ADD COLUMN total_paid REAL DEFAULT 0")
        
        # SQLite ne supporte pas DROP COLUMN directement avant version 3.35.0
        # On va créer une nouvelle table et copier les données
        if 'health' in columns or 'external_club' in columns:
            # Créer une nouvelle table temporaire sans les champs obsolètes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members_new (
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
                    FOREIGN KEY(mjc_club_id) REFERENCES mjc_clubs(id)
                )
            """)
            
            # Copier les données (en excluant les colonnes obsolètes)
            common_columns = [col for col in columns if col not in ['health', 'external_club']]
            # Filtrer pour ne garder que les colonnes qui existent dans la nouvelle table
            new_table_columns = ['id', 'last_name', 'first_name', 'address', 'postal_code', 'city',
                                'phone', 'mail', 'rgpd', 'image_rights', 'payment_type', 
                                'ancv_amount', 'cash_amount', 'check1_amount', 'check2_amount', 
                                'check3_amount', 'total_paid', 'mjc_club_id', 'cotisation_status']
            columns_to_copy = [col for col in common_columns if col in new_table_columns]
            
            if columns_to_copy:
                columns_str = ', '.join(columns_to_copy)
                cursor.execute(f"INSERT INTO members_new ({columns_str}) SELECT {columns_str} FROM members")
                
                # Remplacer l'ancienne table par la nouvelle
                cursor.execute("DROP TABLE members")
                cursor.execute("ALTER TABLE members_new RENAME TO members")
        
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
        Database._current_db_path = None