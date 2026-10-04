# -*- coding: utf-8 -*-
"""Vérifie que le logging fonctionne bout en bout et qu'aucun print() ne subsiste dans core/."""

import ast
import logging
import pathlib

import pytest

from club_manager.core import logger as logmod
from club_manager.core import members, smtp_util
from club_manager.core.database import Database

CORE_DIR = pathlib.Path(__file__).resolve().parent.parent / "club_manager" / "core"


@pytest.fixture
def fresh_logging(tmp_path, monkeypatch):
    """Reconfigure le logging vers un répertoire temporaire puis restaure l'état global."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CLUBMANAGER_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CLUBMANAGER_LOG_LEVEL", "INFO")
    monkeypatch.setattr(logmod, "_configured", False)
    root = logging.getLogger(logmod.LOGGER_NAME)
    old_handlers, old_level = list(root.handlers), root.level
    logmod.setup_logging()
    yield log_dir / logmod.LOG_FILE_NAME
    root.setLevel(old_level)
    for handler in list(root.handlers):
        if handler not in old_handlers:
            root.removeHandler(handler)
            handler.close()


def _flush():
    for handler in logging.getLogger(logmod.LOGGER_NAME).handlers:
        handler.flush()


def test_real_calls_write_to_log_file(fresh_logging, tmp_path):
    database = Database.change_database(str(tmp_path / "log.db"))
    try:
        members.add_member(last_name="Dupont", first_name="Jean")
        smtp_util.SMTPConfig.get_encryption_key()  # journalise l'absence d'APP_SECRET_KEY
        _flush()
        text = fresh_logging.read_text(encoding="utf-8")
        assert "Ouverture de la base" in text
        assert "Membre ajouté: Dupont Jean" in text
        assert "[INFO] clubmanager.database" in text
    finally:
        database.close()


def test_smtp_warning_logged_without_secret(fresh_logging, monkeypatch):
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)
    smtp_util.SMTPConfig.get_encryption_key()
    _flush()
    assert "APP_SECRET_KEY non défini" in fresh_logging.read_text(encoding="utf-8")


def test_rotation_configured(fresh_logging):
    from logging.handlers import RotatingFileHandler

    handlers = [h for h in logging.getLogger(logmod.LOGGER_NAME).handlers if isinstance(h, RotatingFileHandler)]
    assert handlers
    assert handlers[-1].maxBytes == logmod.MAX_BYTES > 0
    assert handlers[-1].backupCount == logmod.BACKUP_COUNT > 0


@pytest.mark.parametrize("path", sorted(CORE_DIR.glob("*.py")), ids=lambda p: p.name)
def test_no_print_in_core(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    prints = [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print"
    ]
    assert not prints, f"print() dans {path.name} lignes {prints}"
