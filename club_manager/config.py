# -*- coding: utf-8 -*-
"""
Configuration centralisée de Club Manager.

Les valeurs peuvent être surchargées par des variables d'environnement
(ou un fichier ``.env``, voir ``.env.example``).
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv est optionnel à l'exécution
    pass


class Config:
    """Accès centralisé aux paramètres de l'application."""

    DEFAULT_DATA_DIR = "~/.clubmanager"
    DEFAULT_DB_NAME = "club_manager.db"
    DEFAULT_LOG_LEVEL = "INFO"

    @classmethod
    def data_dir(cls, create: bool = False) -> str:
        """Retourne le répertoire de données (CLUBMANAGER_DATA_DIR).

        Args:
            create: Crée le répertoire s'il n'existe pas.
        """
        path = os.path.expanduser(os.environ.get("CLUBMANAGER_DATA_DIR", cls.DEFAULT_DATA_DIR))
        if create:
            os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def log_dir(cls) -> str:
        """Retourne le répertoire des logs (CLUBMANAGER_LOG_DIR)."""
        default = os.path.join(cls.data_dir(), "logs")
        return os.path.expanduser(os.environ.get("CLUBMANAGER_LOG_DIR", default))

    @classmethod
    def log_level(cls) -> str:
        """Retourne le niveau de log (CLUBMANAGER_LOG_LEVEL)."""
        return os.environ.get("CLUBMANAGER_LOG_LEVEL", cls.DEFAULT_LOG_LEVEL).upper()

    @classmethod
    def default_db_path(cls) -> str:
        """Retourne le chemin de la base par défaut (CLUBMANAGER_DB_PATH)."""
        return os.environ.get("CLUBMANAGER_DB_PATH", cls.DEFAULT_DB_NAME)

    @classmethod
    def config_file(cls) -> str:
        """Retourne le chemin du fichier de configuration JSON de l'application."""
        return os.path.join(cls.data_dir(), "config.json")

    @classmethod
    def secret_key(cls) -> Optional[str]:
        """Retourne APP_SECRET_KEY (clé de chiffrement SMTP) si définie."""
        return os.environ.get("APP_SECRET_KEY")
