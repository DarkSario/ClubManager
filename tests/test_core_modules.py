# -*- coding: utf-8 -*-
"""Tests des modules métier de club_manager.core (bases temporaires)."""

import os
import zipfile
from datetime import datetime, timedelta

import pytest

from club_manager.core import (
    annual_prices,
    audit,
    auditview,
    backup,
    cotisations,
    custom_fields,
    images,
    imports,
    mailing,
    mailing_advanced,
    members,
    mjc_clubs,
    positions,
    relance,
    rgpd,
    sessions,
    statistics,
    theming,
    utils,
)
from club_manager.core.database import Database


class _Box:
    """Remplace QMessageBox en enregistrant les appels."""

    Yes = 1
    No = 2
    calls = []

    @classmethod
    def _rec(cls, kind):
        def fn(*args, **kwargs):
            cls.calls.append((kind, args))
            return cls.Yes

        return fn


@pytest.fixture
def box(monkeypatch):
    class Box(_Box):
        calls = []

    for kind in ("information", "warning", "critical", "question"):
        setattr(Box, kind, staticmethod(Box._rec(kind)))
    for module in (backup, imports, mailing, mailing_advanced, theming):
        if hasattr(module, "QMessageBox"):
            monkeypatch.setattr(module, "QMessageBox", Box)
    return Box


# --- annual_prices -----------------------------------------------------------------------------


def test_annual_prices(db):
    assert annual_prices.get_current_annual_price() is None
    annual_prices.add_annual_price("2024", 100, 50, is_current=True)
    annual_prices.add_annual_price("2025", 110, 55, is_current=True)
    assert annual_prices.get_current_annual_price()["year"] == "2025"
    assert [r["year"] for r in annual_prices.get_all_annual_prices()] == ["2025", "2024"]
    price = annual_prices.get_annual_price_by_year("2024")
    assert price["club_price"] == 100.0
    assert annual_prices.get_annual_price_by_year("1999") is None
    annual_prices.set_current_annual_price(price["id"])
    assert annual_prices.get_current_annual_price()["year"] == "2024"
    annual_prices.update_annual_price(price["id"], "2024", 120, 60, True)
    assert annual_prices.get_annual_price_by_year("2024")["club_price"] == 120.0
    annual_prices.delete_annual_price(price["id"])
    assert annual_prices.get_annual_price_by_year("2024") is None


# --- mjc_clubs, positions, custom fields -------------------------------------------------------


def test_mjc_clubs(db):
    mjc_clubs.add_mjc_club("Judo")
    mjc_clubs.add_mjc_club("Aïkido")
    assert [c["name"] for c in mjc_clubs.get_all_mjc_clubs()] == ["Aïkido", "Judo"]
    club = mjc_clubs.get_all_mjc_clubs()[1]
    assert mjc_clubs.get_mjc_club_by_id(club["id"])["name"] == "Judo"
    assert mjc_clubs.get_mjc_club_by_id(999) is None
    mjc_clubs.update_mjc_club(club["id"], "Judo 2")
    assert mjc_clubs.get_mjc_club_by_id(club["id"])["name"] == "Judo 2"
    mjc_clubs.delete_mjc_club(club["id"])
    assert len(mjc_clubs.get_all_mjc_clubs()) == 1


def test_positions(db):
    positions.add_position("Président", "bureau", "Dirige")
    pos = positions.get_all_positions()[0]
    assert pos["assigned_to"] is None
    positions.update_position(pos["id"], "Président", "bureau", "Dirige", "Dupont")
    assert positions.get_all_positions()[0]["assigned_to"] == "Dupont"
    positions.delete_position(pos["id"])
    assert positions.get_all_positions() == []


def test_custom_fields(db):
    custom_fields.add_custom_field("Taille", "texte", "M", "", "")
    field = custom_fields.get_all_custom_fields()[0]
    custom_fields.update_custom_field(field["id"], "Taille", "liste", "M", "S,M,L", "")
    assert custom_fields.get_all_custom_fields()[0]["type"] == "liste"
    custom_fields.delete_custom_field(field["id"])
    assert custom_fields.get_all_custom_fields() == []


# --- sessions / cotisations / relance / statistics -----------------------------------------------


@pytest.fixture
def populated(db):
    members.add_member(last_name="Dupont", first_name="Jean", city="Lyon", mail="j@d.fr")
    members.add_member(last_name="Martin", first_name="Paul", city="Lyon", mail="p@m.fr")
    members.add_member(last_name="Durand", first_name="Anne", city="Paris", mail="a@d.fr")
    sessions.add_session("2024-2025", "2024-09-01", "2025-06-30", 100, 50, is_current=True)
    session = sessions.get_all_sessions()[0]
    ids = [m["id"] for m in members.get_all_members()]
    cotisations.add_cotisation(ids[0], session["id"], 100, 100, "2025-01-10", "Espèces", "Payé")
    cotisations.add_cotisation(ids[1], session["id"], 100, 20, None, "Chèque", "En attente", "123")
    return {"ids": ids, "session": session["id"]}


def test_sessions(db):
    sessions.add_session("A", "2024-01-01", "2024-12-31", 1, 2, is_current=True)
    sessions.add_session("B", "2025-01-01", "2025-12-31", 3, 4, is_current=True)
    by_name = {s["name"]: s for s in sessions.get_all_sessions()}
    assert by_name["A"]["is_current"] == 0 and by_name["B"]["is_current"] == 1
    sessions.set_current_session(by_name["A"]["id"])
    assert {s["name"]: s["is_current"] for s in sessions.get_all_sessions()} == {"A": 1, "B": 0}
    sessions.update_session(by_name["B"]["id"], "B2", "2025-01-01", "2025-12-31", 3, 4, True)
    assert {s["name"] for s in sessions.get_all_sessions()} == {"A", "B2"}
    sessions.delete_session(by_name["A"]["id"])
    assert len(sessions.get_all_sessions()) == 1


def test_cotisations(populated):
    assert len(cotisations.get_all_cotisations()) == 2
    late = cotisations.get_late_members()
    assert [m["last_name"] for m in late] == ["Martin"]
    pending = [c for c in cotisations.get_all_cotisations() if c["status"] == "En attente"][0]
    cotisations.update_cotisation(
        pending["id"], pending["member_id"], populated["session"], 100, 100, "2025-02-01", "Chèque", "Payé", "123"
    )
    assert cotisations.get_late_members() == []
    cotisations.delete_cotisation(pending["id"])
    assert len(cotisations.get_all_cotisations()) == 1


def test_relance(populated):
    rows = relance.get_members_to_remind()
    assert [r["last_name"] for r in rows] == ["Martin"]
    assert rows[0]["session_name"] == "2024-2025"
    cot = [c for c in cotisations.get_all_cotisations() if c["status"] == "En attente"][0]
    relance.mark_relance_sent(cot["id"])
    assert [c["status"] for c in cotisations.get_all_cotisations() if c["id"] == cot["id"]] == ["Relancé"]


def test_statistics(populated):
    assert statistics.count_members() == 3
    assert {r["city"]: r["count"] for r in statistics.count_members_by_city()} == {"Lyon": 2, "Paris": 1}
    assert {r["status"]: r["count"] for r in statistics.count_cotisations_by_status()} == {
        "Payé": 1,
        "En attente": 1,
    }
    assert statistics.total_collected_fees() == 120
    history = statistics.session_history()
    assert history[0]["name"] == "2024-2025" and history[0]["nb_adhesions"] == 2


def test_statistics_empty(db):
    assert statistics.count_members() == 0
    assert statistics.total_collected_fees() is None


# --- rgpd / audit ------------------------------------------------------------------------------


def test_rgpd_purge(populated):
    members.add_member(last_name="Ancien", first_name="Vieux", mail="v@v.fr", city="Nice")
    rgpd.purge_rgpd()
    by_name = {m["id"]: m for m in members.get_all_members()}
    assert by_name[populated["ids"][0]]["last_name"] == "Dupont"  # cotisation récente
    anonymised = [m for m in by_name.values() if m["last_name"] == "ANONYMISE"]
    assert len(anonymised) >= 1
    assert all(m["mail"] == "" and m["city"] == "" for m in anonymised)


def test_rgpd_ready(db):
    assert rgpd.is_rgpd_ready({"rgpd": 1})
    assert not rgpd.is_rgpd_ready({"rgpd": None})
    assert not rgpd.is_rgpd_ready({"rgpd": 0})


def test_audit(db):
    audit.log_action("create", "admin", "member", "details 1")
    audit.log_action("delete", "bob", "member", "details 2")
    assert len(audit.get_all_audit_entries()) == 2
    assert len(auditview.get_audit_by_user("bob")) == 1
    assert len(auditview.get_audit_by_action("create")) == 1
    assert len(auditview.get_all_audit_entries()) == 2
    entry = auditview.get_audit_by_user("bob")[0]
    auditview.delete_audit_entry(entry["id"])
    assert len(audit.get_all_audit_entries()) == 1


def test_audit_delete_old(db):
    old = (datetime.now() - timedelta(days=800)).isoformat()
    db.execute("INSERT INTO audit (date, action, user, object, details) VALUES (?,?,?,?,?)", (old, "a", "u", "o", "d"))
    audit.log_action("new", "u", "o", "d")
    audit.delete_old_audit_entries(365)
    assert [e["action"] for e in audit.get_all_audit_entries()] == ["new"]


# --- utils ---------------------------------------------------------------------------------------


def test_utils_validation():
    assert utils.is_email_valid("a@b.fr") and not utils.is_email_valid("abc")
    assert utils.is_phone_valid("06 12 34 56 78") and not utils.is_phone_valid("123")
    assert utils.format_currency(12.5) == "12.50 €"
    assert utils.format_currency("x") == "0.00 €"
    assert utils.safe_str(3) == "3"

    class Bad:
        def __str__(self):
            raise RuntimeError

    assert utils.safe_str(Bad()) == ""


def test_utils_amounts():
    assert utils.safe_get_amount({"a": "2.5"}, "a") == 2.5
    assert utils.safe_get_amount({"a": None}, "a") == 0.0
    assert utils.safe_get_amount({}, "a") == 0.0
    assert utils.safe_get_amount({"a": "x"}, "a") == 0.0
    totals = utils.calculate_payment_totals(
        [
            {"cash_amount": 10, "check1_amount": 5, "check2_amount": 5, "check3_amount": None, "ancv_amount": 2.5},
            {"cash_amount": 1},
        ]
    )
    assert totals == {"total": 23.5, "cash": 11.0, "checks": 10.0, "ancv": 2.5}
    assert utils.calculate_payment_totals([])["total"] == 0.0


def test_calculate_totals_survives_bad_member():
    class Boom:
        def get(self, key):
            raise RuntimeError("x")

        def __getitem__(self, key):
            raise RuntimeError("x")

    # safe_get_amount n'attrape pas RuntimeError : le membre est ignoré
    totals = utils.calculate_payment_totals([Boom(), {"cash_amount": 4}])
    assert totals["cash"] == 4.0


# --- images / theming -------------------------------------------------------------------------


def test_images(tmp_path, monkeypatch):
    monkeypatch.setattr(images, "IMAGE_FOLDER", str(tmp_path / "imgs"))
    assert images.list_images() == []
    src = tmp_path / "logo.png"
    src.write_bytes(b"png")
    dest = images.save_image(str(src), "logo.png")
    assert os.path.exists(dest)
    (tmp_path / "imgs" / "notes.txt").write_text("x")
    assert images.list_images() == ["logo.png"]
    images.delete_image("logo.png")
    images.delete_image("absent.png")
    assert images.list_images() == []


def test_theming(tmp_path, monkeypatch):
    conf = str(tmp_path / "theme.conf")
    assert theming.load_theme_choice(conf) == (None, None)
    theming.save_theme_choice("a.qss", "logo.png", conf)
    assert theming.load_theme_choice(conf) == ("a.qss", "logo.png")

    class App:
        sheet = None

        def setStyleSheet(self, s):
            self.sheet = s

    qss = tmp_path / "a.qss"
    qss.write_text("QWidget {}")
    app = App()
    theming.load_theme(str(tmp_path / "missing.qss"), app)
    assert app.sheet is None
    theming.load_theme(str(qss), app)
    assert app.sheet == "QWidget {}"
    monkeypatch.setattr(theming.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: ("logo.png", "")))
    assert theming.import_logo() == "logo.png"


# --- imports -----------------------------------------------------------------------------------


def test_imports_csv(db, tmp_path, monkeypatch, box):
    csv_file = tmp_path / "m.csv"
    csv_file.write_text("Nom;Prenom\nDupont;Jean\n", encoding="utf-8")
    assert imports.guess_csv_fields(str(csv_file)) == ["Nom;Prenom"]
    csv_file.write_text("Nom,Prenom\nDupont,Jean\nMartin,Paul\n", encoding="utf-8")
    assert imports.guess_csv_fields(str(csv_file)) == ["Nom", "Prenom"]

    monkeypatch.setattr(imports.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: ("", "")))
    imports.import_csv_to_table("members", {"Nom": "last_name"})
    assert members.get_all_members() == []

    monkeypatch.setattr(imports.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (str(csv_file), "")))
    imports.import_csv_to_table("members", {"Nom": "last_name", "Prenom": "first_name"})
    assert sorted(m["last_name"] for m in members.get_all_members()) == ["Dupont", "Martin"]
    assert box.calls[-1][0] == "information"


# --- mailing -----------------------------------------------------------------------------------


class FakeSMTP:
    sent = []
    fail = False

    def __init__(self, host, port):
        self.host, self.port = host, port
        self.tls = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def starttls(self):
        self.tls = True

    def login(self, user, password):
        self.logged = (user, password)

    def sendmail(self, sender, recipients, text):
        if FakeSMTP.fail:
            raise OSError("down")
        FakeSMTP.sent.append((sender, recipients, text))


@pytest.fixture
def fake_smtp(monkeypatch):
    FakeSMTP.sent = []
    FakeSMTP.fail = False
    monkeypatch.setattr(mailing.smtplib, "SMTP", FakeSMTP)
    monkeypatch.setattr(mailing_advanced.smtplib, "SMTP", FakeSMTP)
    return FakeSMTP


CFG = {"host": "h", "from": "club@x.fr", "tls": True, "user": "u", "password": "p"}


def test_send_mailing(fake_smtp, box):
    mailing.send_mailing("Sujet", "Corps", ["a@b.fr", "c@d.fr"], CFG)
    assert fake_smtp.sent[0][1] == ["a@b.fr", "c@d.fr"]
    assert box.calls[-1][0] == "information"
    fake_smtp.fail = True
    mailing.send_mailing("Sujet", "Corps", ["a@b.fr"], CFG)
    assert box.calls[-1][0] == "critical"


def test_mailing_advanced(db, fake_smtp, box, tmp_path):
    members.add_member(last_name="Dupont", first_name="Jean", mail="j@d.fr", rgpd=1)
    members.add_member(last_name="Martin", first_name="Paul", mail=None, rgpd=0)
    all_members = members.get_all_members()
    assert len(mailing_advanced.select_recipients(all_members)) == 2
    assert len(mailing_advanced.select_recipients(all_members, {"rgpd": 1})) == 1
    assert len(mailing_advanced.select_recipients(all_members, {"mail": None})) == 1

    tpl = tmp_path / "t.txt"
    tpl.write_text("Bonjour {first_name} {last_name}", encoding="utf-8")
    template = mailing_advanced.load_template(str(tpl))
    assert mailing_advanced.personalize_template(template, {"first_name": "A", "last_name": "B"}) == "Bonjour A B"

    attachment = tmp_path / "doc.txt"
    attachment.write_text("pj")
    mailing_advanced.send_mass_mail("S", template, all_members[:1], CFG, attachments=[str(attachment), "absent"])
    assert "doc.txt" in fake_smtp.sent[0][2]
    assert box.calls[-1][0] == "information"
    fake_smtp.fail = True
    mailing_advanced.send_mass_mail("S", template, all_members, CFG)
    assert box.calls[-1][0] == "warning"


def test_select_attachments(monkeypatch):
    monkeypatch.setattr(mailing_advanced.QFileDialog, "getOpenFileNames", staticmethod(lambda *a, **k: (["f"], "")))
    assert mailing_advanced.select_attachments() == ["f"]


# --- backup ------------------------------------------------------------------------------------


def test_backup_and_restore(qapp, db, tmp_path, monkeypatch, box):
    members.add_member(last_name="Dupont", first_name="Jean")
    target = str(tmp_path / "save.zip")
    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (target, "")))
    backup.backup_database(db.db_path)
    assert zipfile.is_zipfile(target)
    assert "test.db" in zipfile.ZipFile(target).namelist()

    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: ("", "")))
    backup.backup_database(db.db_path)

    restore_dir = tmp_path / "restore"
    restore_dir.mkdir()
    copy = restore_dir / "save.zip"
    copy.write_bytes(open(target, "rb").read())
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (str(copy), "")))
    backup.restore_database()
    assert (restore_dir / "test.db").exists()
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: ("", "")))
    backup.restore_database()
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (str(tmp_path), "")))
    backup.restore_database()
    assert box.calls[-1][0] == "critical"


def test_export_import_zip_archive(qapp, db, tmp_path, monkeypatch, box):
    import sqlite3

    members.add_member(last_name="Dupont", first_name="Jean")
    assert Database.get_current_db_path() == db.db_path
    target = str(tmp_path / "full")
    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (target, "")))
    backup.export_zip_archive()
    assert zipfile.is_zipfile(target + ".zip")

    restored = str(tmp_path / "restored" / "copy.db")
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (target + ".zip", "")))
    monkeypatch.setattr(backup.QFileDialog, "getSaveFileName", staticmethod(lambda *a, **k: (restored, "")))
    backup.import_zip_archive()
    assert box.calls[-1][0] == "information"
    conn = sqlite3.connect(restored)
    assert conn.execute("SELECT last_name FROM members").fetchone()[0] == "Dupont"
    conn.close()

    empty = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty, "w") as z:
        z.writestr("readme.txt", "x")
    monkeypatch.setattr(backup.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (str(empty), "")))
    backup.import_zip_archive()
    assert box.calls[-1][0] == "warning"
