# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/custom_fields_tab.py
Rôle : Onglet gestion des champs personnalisés (CustomFieldsTab) du Club Manager.
Hérite de QWidget et de Ui_CustomFieldsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CustomFieldsTab généré par pyuic5 à partir de resources/ui/custom_fields_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.custom_fields_tab_ui import Ui_CustomFieldsTab

class CustomFieldsTab(QtWidgets.QWidget, Ui_CustomFieldsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddCustomField.clicked.connect(self.add_custom_field)
        self.buttonEditCustomField.clicked.connect(self.edit_custom_field)
        self.buttonDeleteCustomField.clicked.connect(self.delete_custom_field)
        self.buttonExportCustomFields.clicked.connect(self.export_custom_fields)
        self.tableCustomFields.doubleClicked.connect(self.edit_custom_field)

    def add_custom_field(self):
        from club_manager.ui.custom_field_form_dialog import CustomFieldFormDialog
        dlg = CustomFieldFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_custom_fields()

    def edit_custom_field(self):
        # Logique de modification du champ personnalisé sélectionné
        pass

    def delete_custom_field(self):
        # Logique de suppression du/des champs personnalisés sélectionnés
        pass

    def export_custom_fields(self):
        # Exporter les champs personnalisés
        pass

    def refresh_custom_fields(self):
        # Recharge la table depuis la base
        pass