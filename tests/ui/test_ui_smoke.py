# -*- coding: utf-8 -*-
"""Tests de fumée PyQt5 (headless : QT_QPA_PLATFORM=offscreen). Marqués ``ui``."""

import pytest
from PyQt5 import QtWidgets

from club_manager.core import members

pytestmark = pytest.mark.ui


@pytest.fixture(autouse=True)
def no_blocking_dialogs(monkeypatch):
    """Remplace les QMessageBox/QFileDialog bloquants et enregistre les messages."""
    calls = []
    for kind in ("information", "warning", "critical"):
        monkeypatch.setattr(
            QtWidgets.QMessageBox, kind, staticmethod(lambda *a, _k=kind, **k: calls.append((_k, a)) or 0)
        )
    monkeypatch.setattr(QtWidgets.QMessageBox, "question", staticmethod(lambda *a, **k: QtWidgets.QMessageBox.Yes))
    for name in ("getSaveFileName", "getOpenFileName"):
        monkeypatch.setattr(QtWidgets.QFileDialog, name, staticmethod(lambda *a, **k: ("", "")))
    return calls


def test_main_window(qtbot, db):
    from club_manager.main_window import MainWindow

    window = MainWindow(db_path=db.db_path)
    qtbot.addWidget(window)
    assert window.tabs.count() >= 6
    assert "test.db" in window.windowTitle()


def test_members_tab_load_add_and_filter(qtbot, db, monkeypatch, no_blocking_dialogs):
    from club_manager.ui import member_filter_dialog, member_form_dialog
    from club_manager.ui.members_tab import MembersTab

    members.add_member(last_name="Dupont", first_name="Jean", city="Lyon")
    tab = MembersTab()
    qtbot.addWidget(tab)
    assert tab.tableMembers.rowCount() == 1

    def fill_form(self):
        self.editLastName.setText("Martin")
        self.editFirstName.setText("Paul")
        self.editCity.setText("Paris")
        return QtWidgets.QDialog.Accepted

    monkeypatch.setattr(member_form_dialog.MemberFormDialog, "exec_", fill_form)
    tab.add_member()
    assert [k for k, _ in no_blocking_dialogs][-1] == "information"
    assert {m["last_name"] for m in members.get_all_members()} == {"Dupont", "Martin"}
    assert tab.tableMembers.rowCount() == 2

    def fill_filter(self):
        self.edit_city.setText("Paris")
        return QtWidgets.QDialog.Accepted

    monkeypatch.setattr(member_filter_dialog.MemberFilterDialog, "exec_", fill_filter)
    tab.filter_members()
    assert tab.tableMembers.rowCount() == 1
    assert tab._current_filter == {"city": "Paris"}


def test_members_tab_filter_without_criteria(qtbot, db, monkeypatch, no_blocking_dialogs):
    from club_manager.ui import member_filter_dialog
    from club_manager.ui.members_tab import MembersTab

    tab = MembersTab()
    qtbot.addWidget(tab)
    monkeypatch.setattr(member_filter_dialog.MemberFilterDialog, "exec_", lambda self: QtWidgets.QDialog.Accepted)
    tab.filter_members()
    assert no_blocking_dialogs[-1][0] == "information"


def test_mailing_tab(qtbot, db):
    from club_manager.ui.mailing_tab import MailingTab

    tab = MailingTab()
    qtbot.addWidget(tab)
    assert tab.isEnabled()


def test_exports_tab(qtbot, db):
    from club_manager.ui.exports_tab import ExportsTab

    tab = ExportsTab()
    qtbot.addWidget(tab)
    assert tab.isEnabled()


def test_database_selector_dialog(qtbot):
    from club_manager.ui.database_selector_dialog import DatabaseSelectorDialog

    dlg = DatabaseSelectorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_selected_database_path() is None or isinstance(dlg.get_selected_database_path(), str)


def test_smtp_settings_dialog_warns_without_secret(qtbot, db, monkeypatch):
    from club_manager.ui.smtp_settings_dialog import SMTPSettingsDialog

    monkeypatch.delenv("APP_SECRET_KEY", raising=False)
    dlg = SMTPSettingsDialog()
    qtbot.addWidget(dlg)
    assert dlg.findChild(QtWidgets.QLabel, "secretKeyWarning") is not None

    monkeypatch.setenv("APP_SECRET_KEY", "une-cle-secrete-de-test")
    dlg2 = SMTPSettingsDialog()
    qtbot.addWidget(dlg2)
    assert dlg2.findChild(QtWidgets.QLabel, "secretKeyWarning") is None
