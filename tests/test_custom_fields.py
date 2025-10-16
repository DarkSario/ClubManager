# -*- coding: utf-8 -*-
from club_manager.core.custom_fields import add_custom_field, get_all_custom_fields, delete_custom_field
from club_manager.core.database import Database

def test_add_and_delete_custom_field(tmp_path, monkeypatch):
    dbfile = tmp_path / "cf.db"
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    add_custom_field("Age", "Numérique", "", "", "")
    cfs = get_all_custom_fields()
    assert any(cf["name"] == "Age" for cf in cfs)
    field_id = [cf["id"] for cf in cfs if cf["name"] == "Age"][0]
    delete_custom_field(field_id)
    cfs = get_all_custom_fields()
    assert all(cf["name"] != "Age" for cf in cfs)
    db.close()