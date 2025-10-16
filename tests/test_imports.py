# -*- coding: utf-8 -*-
import csv
import tempfile
from club_manager.core.imports import import_csv_to_table, guess_csv_fields
from club_manager.core.database import Database

def test_guess_csv_fields(tmp_path):
    csvfile = tmp_path / "test.csv"
    with open(csvfile, "w", encoding="utf-8") as f:
        f.write("nom,prenom,ville\nDupont,Marie,Paris\n")
    fields = guess_csv_fields(str(csvfile))
    assert fields == ["nom", "prenom", "ville"]

def test_import_csv_to_table(tmp_path, monkeypatch):
    dbfile = tmp_path / "imp.db"
    csvfile = tmp_path / "in.csv"
    with open(csvfile, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["last_name", "first_name"])
        writer.writeheader()
        writer.writerow({"last_name": "Test", "first_name": "User"})
    monkeypatch.setattr("club_manager.core.database.Database._instance", None)
    db = Database(str(dbfile))
    monkeypatch.setattr("club_manager.core.database.Database.instance", lambda: db)
    # Simule le QFileDialog
    monkeypatch.setattr("PyQt5.QtWidgets.QFileDialog.getOpenFileName", lambda *a, **k: (str(csvfile), ""))
    import_csv_to_table("members", {"last_name": "last_name", "first_name": "first_name"}, parent=None)
    rows = db.query("SELECT * FROM members WHERE last_name='Test'")
    assert rows
    db.close()