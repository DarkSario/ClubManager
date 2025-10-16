# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/sessions_tab.py
Rôle : Onglet gestion des sessions (SessionsTab) du Club Manager.
Hérite de QWidget et de Ui_SessionsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_SessionsTab généré par pyuic5 à partir de resources/ui/sessions_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.sessions_tab_ui import Ui_SessionsTab

class SessionsTab(QtWidgets.QWidget, Ui_SessionsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddSession.clicked.connect(self.add_session)
        self.buttonEditSession.clicked.connect(self.edit_session)
        self.buttonDeleteSession.clicked.connect(self.delete_session)
        self.buttonExportSessions.clicked.connect(self.export_sessions)
        self.tableSessions.doubleClicked.connect(self.edit_session)
        self.buttonSetCurrent.clicked.connect(self.set_current_session)

    def add_session(self):
        from club_manager.ui.session_form_dialog import SessionFormDialog
        dlg = SessionFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_sessions()

    def edit_session(self):
        # Logique de modification de la session sélectionnée
        pass

    def delete_session(self):
        # Logique de suppression de la/des sessions sélectionnées
        pass

    def export_sessions(self):
        # Exporter les sessions
        pass

    def set_current_session(self):
        # Définir la session courante
        pass

    def refresh_sessions(self):
        # Recharge la table depuis la base
        pass