# -*- coding: utf-8 -*-
from club_manager.core.statistics import count_members, count_members_by_city, count_cotisations_by_status, total_collected_fees, session_history
from club_manager.core.database import Database

def test_statistics(tmp_path, monkeypatch):
    dbfile = tmp_path / "stat.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    db.execute("INSERT INTO members (last_name, first_name, city) VALUES (?, ?, ?)", ("A", "B", "C"))
    db.execute("INSERT INTO cotisations (member_id, session_id, amount, paid, status) VALUES (?, ?, ?, ?, ?)", (1, 1, 100, 100, "Payé"))
    db.execute("INSERT INTO sessions (name, start, end, club_amount, mjc_amount, is_current) VALUES (?, ?, ?, ?, ?, ?)", ("S1", "2020-01-01", "2020-12-31", 100, 20, 1))
    assert count_members() == 1
    assert count_members_by_city()[0]["city"] == "C"
    assert count_cotisations_by_status()[0]["status"] == "Payé"
    assert total_collected_fees() == 100
    assert session_history()
    db.close()