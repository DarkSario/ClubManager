# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/custom_field_form_dialog.ui
Classe : Ui_CustomFieldFormDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_CustomFieldFormDialog(object):
    def setupUi(self, CustomFieldFormDialog):
        CustomFieldFormDialog.setObjectName("CustomFieldFormDialog")
        CustomFieldFormDialog.resize(400, 230)
        self.verticalLayout = QtWidgets.QVBoxLayout(CustomFieldFormDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.editName = QtWidgets.QLineEdit(CustomFieldFormDialog)
        self.formLayout.addRow("Nom du champ :", self.editName)
        self.comboType = QtWidgets.QComboBox(CustomFieldFormDialog)
        self.comboType.addItems(["Texte", "Numérique", "Date", "Choix", "Booléen"])
        self.formLayout.addRow("Type :", self.comboType)
        self.editDefault = QtWidgets.QLineEdit(CustomFieldFormDialog)
        self.formLayout.addRow("Valeur par défaut :", self.editDefault)
        self.editOptions = QtWidgets.QLineEdit(CustomFieldFormDialog)
        self.editOptions.setPlaceholderText("Séparés par virgules")
        self.editOptions.setEnabled(False)
        self.formLayout.addRow("Options (si Choix) :", self.editOptions)
        self.editConstraints = QtWidgets.QLineEdit(CustomFieldFormDialog)
        self.formLayout.addRow("Contraintes :", self.editConstraints)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CustomFieldFormDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)