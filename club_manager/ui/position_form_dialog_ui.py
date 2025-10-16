# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/position_form_dialog.ui
Classe : Ui_PositionFormDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_PositionFormDialog(object):
    def setupUi(self, PositionFormDialog):
        PositionFormDialog.setObjectName("PositionFormDialog")
        PositionFormDialog.resize(400, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(PositionFormDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.editName = QtWidgets.QLineEdit(PositionFormDialog)
        self.formLayout.addRow("Nom du poste :", self.editName)
        self.comboType = QtWidgets.QComboBox(PositionFormDialog)
        self.comboType.addItems(["Staff", "Gestion", "Trésorier", "Président", "Autre"])
        self.formLayout.addRow("Type :", self.comboType)
        self.editDescription = QtWidgets.QLineEdit(PositionFormDialog)
        self.formLayout.addRow("Description :", self.editDescription)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(PositionFormDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)