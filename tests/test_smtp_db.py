# -*- coding: utf-8 -*-
"""Tests de la persistance de la configuration SMTP."""

from club_manager.core.smtp_util import SMTPConfig, get_smtp_config_from_db, save_smtp_config_to_db


def test_no_config(db):
    assert get_smtp_config_from_db() is None


def test_save_and_load(db):
    cfg = SMTPConfig("smtp.example.com", 465, "ssl", "user", "secret", "from@example.com")
    assert save_smtp_config_to_db(cfg) is True
    stored = db.query("SELECT value FROM settings WHERE key='smtp_password'")[0]["value"]
    assert stored != "secret"
    loaded = get_smtp_config_from_db()
    assert loaded.host == "smtp.example.com"
    assert loaded.port == 465
    assert loaded.password == "secret"


def test_undecryptable_password(db):
    cfg = SMTPConfig("h", 25, "none", "u", "p", "f@example.com")
    save_smtp_config_to_db(cfg)
    db.execute("UPDATE settings SET value='garbage' WHERE key='smtp_password'")
    assert get_smtp_config_from_db().password == ""
