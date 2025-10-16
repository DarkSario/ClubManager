# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/session_form_dialog.py
Rôle : Fenêtre modale d'ajout/édition de session.
Hérite de QDialog et Ui_SessionFormDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_SessionFormDialog généré par pyuic5 à partir de resources/ui/session_form_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.session_form_dialog_ui import Ui_SessionFormDialog

class SessionFormDialog(QtWidgets.QDialog, Ui_SessionFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        # Validation minimal
        if not self.editSessionName.text():
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le nom de la session est obligatoire.")
            return
        super().accept()