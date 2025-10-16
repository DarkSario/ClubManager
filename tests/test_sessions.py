# -*- coding: utf-8 -*-
from club_manager.core.sessions import add_session, get_all_sessions, set_current_session
from club_manager.core.database import Database

def test_add_and_set_current_session(tmp_path, monkeypatch):
    dbfile = tmp_path / "sess.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    add_session("2023/2024", "2023-09-01", "2024-06-30", 120, 25, is_current=True)
    add_session("2024/2025", "2024-09-01", "2025-06-30", 130, 30, is_current=False)
    set_current_session(2)
    sess = get_all_sessions()
    current = [s for s in sess if s["is_current"]][0]
    assert current["name"] == "2024/2025"
    db.close()