# -*- coding: utf-8 -*-
import os
import tempfile
import pytest
from club_manager.core.database import Database

@pytest.fixture
def db():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = Database(path)
    yield db
    db.close()
    os.remove(path)

def test_schema_creation(db):
    # Test presence of a table
    tables = db.query("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [t["name"] for t in tables]
    assert "members" in table_names
    assert "cotisations" in table_names

def test_insert_and_query_member(db):
    db.execute("INSERT INTO members (last_name, first_name) VALUES (?, ?)", ("Durand", "Paul"))
    rows = db.query("SELECT * FROM members WHERE last_name=?", ("Durand",))
    assert len(rows) == 1
    assert rows[0]["first_name"] == "Paul"