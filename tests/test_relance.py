# -*- coding: utf-8 -*-
from club_manager.core.relance import get_members_to_remind, mark_relance_sent
from club_manager.core.database import Database

def test_get_members_to_remind_and_mark(tmp_path, monkeypatch):
    dbfile = tmp_path / "relance.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    db.execute("INSERT INTO members (last_name, first_name) VALUES (?, ?)", ("R", "L"))
    db.execute("INSERT INTO sessions (name, start, end, club_amount, mjc_amount, is_current) VALUES (?, ?, ?, ?, ?, ?)", ("2024", "2024-01-01", "2024-12-31", 100, 10, 1))
    db.execute("INSERT INTO cotisations (member_id, session_id, amount, paid, status) VALUES (?, ?, ?, ?, ?)", (1, 1, 100, 0, "En attente"))
    members = get_members_to_remind()
    assert any(m["last_name"] == "R" for m in members)
    mark_relance_sent(1)
    cots = db.query("SELECT status FROM cotisations WHERE id=1")
    assert cots[0]["status"] == "Relancé"
    db.close()