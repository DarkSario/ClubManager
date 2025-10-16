# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/audit_details_dialog.ui
Classe : Ui_AuditDetailsDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_AuditDetailsDialog(object):
    def setupUi(self, AuditDetailsDialog):
        AuditDetailsDialog.setObjectName("AuditDetailsDialog")
        AuditDetailsDialog.resize(500, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(AuditDetailsDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.labelDate = QtWidgets.QLabel(AuditDetailsDialog)
        self.formLayout.addRow("Date :", self.labelDate)
        self.labelAction = QtWidgets.QLabel(AuditDetailsDialog)
        self.formLayout.addRow("Action :", self.labelAction)
        self.labelUser = QtWidgets.QLabel(AuditDetailsDialog)
        self.formLayout.addRow("Utilisateur :", self.labelUser)
        self.labelObject = QtWidgets.QLabel(AuditDetailsDialog)
        self.formLayout.addRow("Objet :", self.labelObject)
        self.verticalLayout.addLayout(self.formLayout)
        self.textDetails = QtWidgets.QTextEdit(AuditDetailsDialog)
        self.textDetails.setReadOnly(True)
        self.textDetails.setPlaceholderText("Détails de l'action...")
        self.verticalLayout.addWidget(self.textDetails)
        self.buttonBox = QtWidgets.QDialogButtonBox(AuditDetailsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)