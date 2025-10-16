# -*- coding: utf-8 -*-
from club_manager.core.rgpd import purge_rgpd, is_rgpd_ready
from club_manager.core.database import Database

def test_purge_rgpd(tmp_path, monkeypatch):
    dbfile = tmp_path / "rgpd.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    db.execute("INSERT INTO members (last_name, first_name, rgpd) VALUES (?, ?, ?)", ("Test", "RGPD", 1))
    purge_rgpd()
    rows = db.query("SELECT * FROM members")
    assert rows[0]["last_name"] in ("ANONYMISE", "Test")
    db.close()

def test_is_rgpd_ready():
    member = {"rgpd": 1}
    assert is_rgpd_ready(member)
    member = {"rgpd": 0}
    assert not is_rgpd_ready(member)