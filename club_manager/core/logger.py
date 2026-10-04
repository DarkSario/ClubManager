# -*- coding: utf-8 -*-
"""
Système de logging centralisé de Club Manager.

Les logs sont écrits dans ``~/.clubmanager/logs/clubmanager.log`` avec rotation
automatique (voir ``club_manager.config.Config``).
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from club_manager.config import Config

LOGGER_NAME = "clubmanager"
LOG_FILE_NAME = "clubmanager.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
MAX_BYTES = 1_000_000
BACKUP_COUNT = 5

_configured = False


def setup_logging() -> logging.Logger:
    """Configure (une seule fois) le logger racine de l'application.

    Returns:
        Le logger ``clubmanager``.
    """
    global _configured
    root = logging.getLogger(LOGGER_NAME)
    if _configured:
        return root

    root.setLevel(getattr(logging, Config.log_level(), logging.INFO))
    formatter = logging.Formatter(LOG_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    try:
        log_dir = Config.log_dir()
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, LOG_FILE_NAME),
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    except OSError:
        root.warning("Impossible de créer le fichier de log, console uniquement")

    _configured = True
    return root


def get_logger(name: str) -> logging.Logger:
    """Retourne un logger enfant (ex: ``clubmanager.database``).

    Args:
        name: Nom du module (ex: ``__name__`` ou ``database``).
    """
    setup_logging()
    return logging.getLogger(f"{LOGGER_NAME}.{name.split('.')[-1]}")
