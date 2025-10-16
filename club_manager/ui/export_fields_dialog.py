# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/export_fields_dialog.py
Rôle : Fenêtre modale de sélection des champs à exporter.
Hérite de QDialog et Ui_ExportFieldsDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ExportFieldsDialog généré par pyuic5 à partir de resources/ui/export_fields_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.export_fields_dialog_ui import Ui_ExportFieldsDialog

class ExportFieldsDialog(QtWidgets.QDialog, Ui_ExportFieldsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Connexion logique si besoin
        self.checkAllFields.toggled.connect(self.toggle_all_fields)

    def toggle_all_fields(self, checked):
        for i in range(self.listFields.count()):
            item = self.listFields.item(i)
            item.setCheckState(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)