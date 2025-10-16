# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/custom_fields_tab.ui
Classe : Ui_CustomFieldsTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_CustomFieldsTab(object):
    def setupUi(self, CustomFieldsTab):
        CustomFieldsTab.setObjectName("CustomFieldsTab")
        CustomFieldsTab.resize(700, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(CustomFieldsTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonAddCustomField = QtWidgets.QPushButton(CustomFieldsTab)
        self.buttonAddCustomField.setText("Ajouter")
        self.buttonEditCustomField = QtWidgets.QPushButton(CustomFieldsTab)
        self.buttonEditCustomField.setText("Modifier")
        self.buttonDeleteCustomField = QtWidgets.QPushButton(CustomFieldsTab)
        self.buttonDeleteCustomField.setText("Supprimer")
        self.buttonExportCustomFields = QtWidgets.QPushButton(CustomFieldsTab)
        self.buttonExportCustomFields.setText("Exporter")
        self.horizontalLayoutTop.addWidget(self.buttonAddCustomField)
        self.horizontalLayoutTop.addWidget(self.buttonEditCustomField)
        self.horizontalLayoutTop.addWidget(self.buttonDeleteCustomField)
        self.horizontalLayoutTop.addWidget(self.buttonExportCustomFields)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tableCustomFields = QtWidgets.QTableWidget(CustomFieldsTab)
        self.tableCustomFields.setColumnCount(4)
        self.tableCustomFields.setHorizontalHeaderLabels([
            "Nom", "Type", "Défaut", "Contraintes"
        ])
        self.verticalLayout.addWidget(self.tableCustomFields)