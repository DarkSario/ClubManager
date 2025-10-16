# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/error_dialog.py
Rôle : Fenêtre modale d'affichage d'une erreur critique ou bloquante.
Hérite de QDialog et Ui_ErrorDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ErrorDialog généré par pyuic5 à partir de resources/ui/error_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.error_dialog_ui import Ui_ErrorDialog

class ErrorDialog(QtWidgets.QDialog, Ui_ErrorDialog):
    def __init__(self, parent=None, error_message="Une erreur est survenue."):
        super().__init__(parent)
        self.setupUi(self)
        self.labelError.setText(error_message)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)