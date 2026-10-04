# -*- coding: utf-8 -*-
"""Scénarios bout en bout (sans UI) : base, membres, filtres, exports, sauvegarde, migration, SMTP, RGPD."""

import csv
import smtplib
import sqlite3
import zipfile

import pytest

from club_manager.core import annual_prices, audit, backup, cotisations, export, members, rgpd, smtp_util
from club_manager.core.database import Database
from club_manager.core.smtp_util import SMTPConfig, SMTPSender


@pytest.fixture
def messages(monkeypatch):
    class Box:
        Yes = 1
        No = 2
        calls = []

        @staticmethod
        def information(*a, **k):
            Box.calls.append("information")

        @staticmethod
        def warning(*a, **k):
            Box.calls.append("warning")

        @staticmethod
        def critical(*a, **k):
            Box.calls.append("critical")

    for module in (export, backup):
        monkeypatch.setattr(module, "QMessageBox", Box)
    return Box


def test_database_prices_members_filters_lifecycle(db):
    annual_prices.add_annual_price("2025", 100, 40, is_current=True)
    assert annual_prices.get_current_annual_price()["club_price"] == 100.0

    members.add_member(last_name="Dupont", first_name="Jean", city="Lyon", rgpd=1, image_rights=0)
    members.add_member(last_name="Martin", first_name="Paul", city="Paris", rgpd=0, image_rights=1)
    members.add_member(last_name="Durand", first_name="Anne", city="Lyon", rgpd=1, image_rights=1)
    assert len(members.get_all_members()) == 3

    lyon = members.get_filtered_members({"city": "Lyon"})
    assert {m["last_name"] for m in lyon} == {"Dupont", "Durand"}
    assert len(members.get_filtered_members({"city": "Lyon", "image_rights": 1})) == 1

    paul = members.get_filtered_members({"first_name": "Paul"})[0]
    members.update_member(paul["id"], city="Nantes", cotisation_status="Payé")
    assert members.get_member_by_id(paul["id"])["city"] == "Nantes"
    assert len(members.get_filtered_members({"cotisation_status": "Payé"})) == 1

    members.delete_member(paul["id"])
    assert members.get_member_by_id(paul["id"]) is None
    assert len(members.get_all_members()) == 2

    with pytest.raises(ValueError):
        members.get_filtered_members({"ville": "Lyon"})
    with pytest.raises(ValueError):
        members.add_member(nom="x")


def test_export_csv_and_pdf(db, tmp_path, monkeypatch, messages):
    members.add_member(last_name="Dupont", first_name="Jean", city="Lyon", rgpd=1)
    members.add_member(last_name="Martin", first_name="Paul", city="Paris", rgpd=0)
    rows = members.get_all_members()

    csv_path = tmp_path / "membres.csv"
    count = export.export_to_csv(rows, str(csv_path), selected_fields=["last_name", "first_name", "rgpd"])
    assert count == 2
    with open(csv_path, newline="", encoding="utf-8") as f:
        content = list(csv.reader(f, delimiter=";"))
    assert len(content[0]) == 3 and content[0][0] == "Nom"
    assert content[1][:2] == ["Dupont", "Jean"] and content[1][2] == "Oui"
    assert content[2][2] == "Non"

    pdf_path = tmp_path / "membres.pdf"
    monkeypatch.setattr(export.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (str(pdf_path), "")))
    assert export.export_to_pdf(rows, "Membres", ["last_name", "first_name", "city"]) is True
    raw = pdf_path.read_bytes()
    assert raw.startswith(b"%PDF") and raw.rstrip().endswith(b"%%EOF")
    assert messages.calls[-1] == "information"


def test_backup_zip_then_restore(qapp, db, tmp_path, monkeypatch, messages):
    members.add_member(last_name="Dupont", first_name="Jean")
    archive = str(tmp_path / "backup.zip")
    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (archive, "")))
    backup.export_zip_archive()
    with zipfile.ZipFile(archive) as z:
        assert "test.db" in z.namelist()

    members.add_member(last_name="Ajout", first_name="Apres")  # modifié après la sauvegarde
    restored = str(tmp_path / "restore" / "restored.db")
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (archive, "")))
    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (restored, "")))
    backup.import_zip_archive()

    reopened = Database.change_database(restored)
    assert [m["last_name"] for m in reopened.query("SELECT last_name FROM members")] == ["Dupont"]


def test_migrate_legacy_database(tmp_path):
    path = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(path))
    conn.execute(
        "CREATE TABLE members (id INTEGER PRIMARY KEY AUTOINCREMENT, last_name TEXT, first_name TEXT, "
        "health TEXT, external_club TEXT, mail TEXT)"
    )
    conn.execute("INSERT INTO members (last_name, first_name, health, external_club) VALUES ('Dupont','Jean','x','y')")
    conn.commit()
    conn.close()

    database = Database.change_database(str(path))
    try:
        cols = [r["name"] for r in database.query("PRAGMA table_info(members)")]
        assert "health" not in cols and "external_club" not in cols and "birth_date" in cols
        assert members.get_all_members()[0]["last_name"] == "Dupont"
        assert database.query("PRAGMA user_version")[0][0] >= 3
    finally:
        database.close()


class FakeServer:
    instances = []
    fail_times = 0
    attempts = 0

    def __init__(self, *args, **kwargs):
        self.messages = []
        FakeServer.instances.append(self)

    def starttls(self):
        pass

    def login(self, user, password):
        pass

    def send_message(self, msg):
        FakeServer.attempts += 1
        if FakeServer.attempts <= FakeServer.fail_times:
            raise smtplib.SMTPServerDisconnected("coupé")
        self.messages.append(msg)

    def quit(self):
        pass


@pytest.fixture
def smtp(monkeypatch, db):
    FakeServer.instances, FakeServer.fail_times, FakeServer.attempts = [], 0, 0
    monkeypatch.setattr(smtp_util.smtplib, "SMTP", FakeServer)
    monkeypatch.setattr(smtp_util.smtplib, "SMTP_SSL", FakeServer)
    monkeypatch.setattr(smtp_util.time, "sleep", lambda s: None)
    config = SMTPConfig("smtp.test", 587, "starttls", "u", "p", "club@test.fr", max_retries=2, batch_size=2)
    return SMTPSender(config)


def _recipient(email, i=1):
    return {"id": i, "email": email, "first_name": "A", "last_name": "B"}


def test_smtp_success_and_logs(smtp):
    result = smtp.send_bulk_email("Sujet", "Corps", [_recipient("a@b.fr"), _recipient("c@d.fr", 2)])
    assert len(result["sent"]) == 2 and not result["failed"]
    assert FakeServer.instances[0].messages[0]["To"] == "a@b.fr"
    logs = Database.instance().query("SELECT status FROM mailing_logs")
    assert [r["status"] for r in logs] == ["sent", "sent"]


def test_smtp_invalid_address(smtp):
    result = smtp.send_bulk_email("S", "C", [_recipient("pas-une-adresse")])
    assert result["failed"][0]["error"] == "Adresse email invalide"
    assert FakeServer.attempts == 0


def test_smtp_retry_then_success(smtp):
    FakeServer.fail_times = 2
    result = smtp.send_bulk_email("S", "C", [_recipient("a@b.fr")])
    assert len(result["sent"]) == 1 and FakeServer.attempts == 3


def test_smtp_failure_after_retries(smtp):
    FakeServer.fail_times = 99
    result = smtp.send_bulk_email("S", "C", [_recipient("a@b.fr")])
    assert len(result["failed"]) == 1 and FakeServer.attempts == 3
    logs = Database.instance().query("SELECT status, error FROM mailing_logs")
    assert logs[0]["status"] == "failed" and "coupé" in logs[0]["error"]


def test_smtp_connection_and_test_email(smtp):
    assert smtp.test_connection() == (True, "Connexion SMTP réussie")
    ok, _ = smtp.send_test_email("me@test.fr")
    assert ok is True


def test_rgpd_purge_scenario(db):
    from club_manager.core import sessions

    members.add_member(last_name="Actif", first_name="A", mail="a@a.fr")
    members.add_member(last_name="Inactif", first_name="B", mail="b@b.fr")
    sessions.add_session("S", "2024-01-01", "2024-12-31", 1, 1, True)
    sid = sessions.get_all_sessions()[0]["id"]
    ids = {m["last_name"]: m["id"] for m in members.get_all_members()}
    cotisations.add_cotisation(ids["Actif"], sid, 10, 10, "2999-01-01", "Espèces", "Payé")
    cotisations.add_cotisation(ids["Inactif"], sid, 10, 10, "2000-01-01", "Espèces", "Payé")
    rgpd.purge_rgpd()
    names = {m["id"]: m for m in members.get_all_members()}
    assert names[ids["Actif"]]["last_name"] == "Actif"
    assert names[ids["Inactif"]]["last_name"] == "ANONYMISE" and names[ids["Inactif"]]["mail"] == ""
    audit.log_action("purge_rgpd", "admin", "members", "test")
    assert audit.get_all_audit_entries()[0]["action"] == "purge_rgpd"
