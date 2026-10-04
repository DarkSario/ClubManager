# -*- coding: utf-8 -*-
"""Tests de Config et du logger."""

import os

from club_manager.config import Config
from club_manager.core import logger as logmod


def test_config_env(monkeypatch, tmp_path):
    monkeypatch.setenv("CLUBMANAGER_DATA_DIR", str(tmp_path / "d"))
    monkeypatch.delenv("CLUBMANAGER_LOG_DIR", raising=False)
    monkeypatch.setenv("CLUBMANAGER_LOG_LEVEL", "debug")
    assert Config.data_dir() == str(tmp_path / "d")
    assert not os.path.exists(Config.data_dir())
    assert os.path.isdir(Config.data_dir(create=True))
    assert Config.log_dir() == os.path.join(str(tmp_path / "d"), "logs")
    assert Config.log_level() == "DEBUG"
    assert Config.config_file().endswith("config.json")


def test_config_defaults(monkeypatch):
    monkeypatch.delenv("CLUBMANAGER_DB_PATH", raising=False)
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)
    assert Config.default_db_path() == "club_manager.db"
    assert Config.secret_key() is None


def test_logger_writes_file(tmp_path, monkeypatch):
    monkeypatch.setenv("CLUBMANAGER_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setattr(logmod, "_configured", False)
    root = logmod.logging.getLogger(logmod.LOGGER_NAME)
    old = list(root.handlers)
    old_level = root.level
    try:
        log = logmod.get_logger("club_manager.core.demo")
        assert log.name == "clubmanager.demo"
        log.error("hello")
        for h in root.handlers:
            h.flush()
        content = (tmp_path / "logs" / "clubmanager.log").read_text(encoding="utf-8")
        assert "hello" in content
    finally:
        root.setLevel(old_level)
        for h in list(root.handlers):
            if h not in old:
                root.removeHandler(h)
                h.close()
