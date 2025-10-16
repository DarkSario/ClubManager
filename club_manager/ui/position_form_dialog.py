# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/position_form_dialog.py
Rôle : Fenêtre modale d'ajout/édition d'un poste.
Hérite de QDialog et Ui_PositionFormDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_PositionFormDialog généré par pyuic5 à partir de resources/ui/position_form_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.position_form_dialog_ui import Ui_PositionFormDialog

class PositionFormDialog(QtWidgets.QDialog, Ui_PositionFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # TODO: Ajoutez la logique de validation, etc.

    def accept(self):
        # Validation des champs (exemple minimal)
        if not self.editName.text():
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le nom du poste est obligatoire.")
            return
        super().accept()