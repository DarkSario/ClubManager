# -*- coding: utf-8 -*-
"""Tests des exports CSV et utilitaires."""

import pytest

from club_manager.core import export
from club_manager.core.export import (
    export_selected_csv,
    export_to_csv,
    get_french_field_name,
    preview_export,
    resolve_mjc_club_names,
)


@pytest.fixture
def clubs(monkeypatch):
    monkeypatch.setattr(export, "get_all_mjc_clubs", lambda: [{"id": 1, "name": "Judo"}, {"id": 2, "name": "Yoga"}])


def test_french_names():
    assert get_french_field_name("last_name") == "Nom"
    assert get_french_field_name("some_field") == "Some Field"


def test_resolve_names(clubs):
    data = [
        {"mjc_club_id": 1, "other_mjc_clubs": "[1, 2]"},
        {"mjc_club_id": 3, "other_mjc_clubs": "1,abc,2"},
        {"mjc_club_id": None, "other_mjc_clubs": ""},
    ]
    out = resolve_mjc_club_names(data)
    assert out[0] == {"mjc_club_id": "Judo", "other_mjc_clubs": "Judo, Yoga"}
    assert out[1]["mjc_club_id"] == "3"
    assert out[1]["other_mjc_clubs"] == "Judo, Yoga"
    assert data[0]["mjc_club_id"] == 1


def test_export_to_csv(tmp_path, clubs):
    path = tmp_path / "out.csv"
    n = export_to_csv([{"last_name": "Dupont", "rgpd": 1, "city": None}], str(path))
    assert n == 1
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "Nom;Consentement RGPD;Ville"
    assert lines[1] == "Dupont;Oui;"


def test_export_to_csv_options(tmp_path, clubs):
    path = tmp_path / "out.csv"
    export_to_csv(
        [{"a": 1, "b": 2}], str(path), delimiter=",", add_bom=True, selected_fields=["b"], translate_headers=False
    )
    raw = path.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")
    assert raw.decode("utf-8-sig").splitlines() == ["b", "2"]


def test_export_to_csv_empty(tmp_path):
    with pytest.raises(ValueError):
        export_to_csv([], str(tmp_path / "x.csv"))


def test_export_sqlite_rows(tmp_path, db, clubs):
    db.execute("INSERT INTO members (last_name, mjc_club_id) VALUES ('Dupont', 1)")
    rows = db.query("SELECT last_name, mjc_club_id FROM members")
    path = tmp_path / "rows.csv"
    export_to_csv(rows, str(path))
    assert "Judo" in path.read_text(encoding="utf-8")


def test_preview_and_selected(tmp_path):
    data = [{"a": 1, "b": 2}]
    assert list(preview_export(data, ["a"]).columns) == ["a"]
    assert list(preview_export(data, []).columns) == ["a", "b"]
    path = tmp_path / "sel.csv"
    export_selected_csv(data, ["b"], str(path))
    assert path.read_text(encoding="utf-8").split() == ["b", "2"]
