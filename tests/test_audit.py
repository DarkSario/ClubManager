# -*- coding: utf-8 -*-
from club_manager.core.audit import log_action
from club_manager.core.database import Database

def test_log_action(tmp_path, monkeypatch):
    dbfile = tmp_path / "audit.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    log_action("MODIF", "admin", "members", "Test modification")
    rows = db.query("SELECT * FROM audit WHERE action='MODIF'")
    assert rows
    db.close()