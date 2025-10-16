# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/confirmation_dialog.py
Rôle : Fenêtre modale de confirmation (suppression, actions critiques).
Hérite de QDialog et Ui_ConfirmationDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ConfirmationDialog généré par pyuic5 à partir de resources/ui/confirmation_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.confirmation_dialog_ui import Ui_ConfirmationDialog

class ConfirmationDialog(QtWidgets.QDialog, Ui_ConfirmationDialog):
    def __init__(self, parent=None, message="Confirmer l'action ?"):
        super().__init__(parent)
        self.setupUi(self)
        self.labelMessage.setText(message)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)