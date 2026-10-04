# -*- coding: utf-8 -*-
"""Fixtures pytest partagées."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from club_manager.core.database import Database  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_dirs(tmp_path, monkeypatch):
    """Isole les répertoires de données/logs de l'utilisateur."""
    monkeypatch.setenv("CLUBMANAGER_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("CLUBMANAGER_LOG_DIR", str(tmp_path / "logs"))


@pytest.fixture
def db(tmp_path):
    """Base SQLite temporaire installée comme instance active."""
    database = Database.change_database(str(tmp_path / "test.db"))
    yield database
    database.close()
