# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/cotisation_form_dialog.ui
Classe : Ui_CotisationFormDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_CotisationFormDialog(object):
    def setupUi(self, CotisationFormDialog):
        CotisationFormDialog.setObjectName("CotisationFormDialog")
        CotisationFormDialog.resize(400, 260)
        self.verticalLayout = QtWidgets.QVBoxLayout(CotisationFormDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.editMember = QtWidgets.QLineEdit(CotisationFormDialog)
        self.formLayout.addRow("Membre :", self.editMember)
        self.editSession = QtWidgets.QLineEdit(CotisationFormDialog)
        self.formLayout.addRow("Session :", self.editSession)
        self.editAmount = QtWidgets.QLineEdit(CotisationFormDialog)
        self.formLayout.addRow("Montant :", self.editAmount)
        self.editPaid = QtWidgets.QLineEdit(CotisationFormDialog)
        self.formLayout.addRow("Payé :", self.editPaid)
        self.datePaiement = QtWidgets.QDateEdit(CotisationFormDialog)
        self.datePaiement.setCalendarPopup(True)
        self.formLayout.addRow("Date paiement :", self.datePaiement)
        self.comboMethod = QtWidgets.QComboBox(CotisationFormDialog)
        self.comboMethod.addItems(["Chèque", "Espèce", "ANCV", "Virement", "Autre"])
        self.formLayout.addRow("Méthode :", self.comboMethod)
        
        self.editChequeNumber = QtWidgets.QLineEdit(CotisationFormDialog)
        self.editChequeNumber.setPlaceholderText("Numéro de chèque (si méthode chèque)")
        self.editChequeNumber.setEnabled(True)
        self.editChequeNumber.hide()
        self.formLayout.addRow("Numéro de chèque :", self.editChequeNumber)
        
        self.comboStatus = QtWidgets.QComboBox(CotisationFormDialog)
        self.comboStatus.addItems(["Payé", "En attente", "Partiel", "Relancé"])
        self.formLayout.addRow("Statut :", self.comboStatus)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CotisationFormDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)