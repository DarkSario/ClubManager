# -*- coding: utf-8 -*-
import pytest
from club_manager.core.database import Database
from club_manager.core.members import add_member, get_all_members, delete_member

@pytest.fixture
def db(tmp_path, monkeypatch):
    dbfile = tmp_path / "test.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    yield db
    db.close()

def test_add_and_delete_member(db, monkeypatch):
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    add_member(last_name="Test", first_name="User")
    members = get_all_members()
    assert any(m["last_name"] == "Test" for m in members)
    member_id = [m["id"] for m in members if m["last_name"] == "Test"][0]
    delete_member(member_id)
    members = get_all_members()
    assert all(m["last_name"] != "Test" for m in members)