# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/custom_field_form_dialog.py
Rôle : Fenêtre modale d'ajout/édition de champ personnalisé.
Hérite de QDialog et Ui_CustomFieldFormDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CustomFieldFormDialog généré par pyuic5 à partir de resources/ui/custom_field_form_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.custom_field_form_dialog_ui import Ui_CustomFieldFormDialog

class CustomFieldFormDialog(QtWidgets.QDialog, Ui_CustomFieldFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Connexion : type change => options dynamiques
        self.comboType.currentTextChanged.connect(self.change_type)

    def change_type(self, type_str):
        # Afficher/masquer options selon type
        if type_str == "Choix":
            self.editOptions.setEnabled(True)
        else:
            self.editOptions.setEnabled(False)
            self.editOptions.clear()

    def accept(self):
        # Validation minimal
        if not self.editName.text():
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le nom du champ est obligatoire.")
            return
        super().accept()