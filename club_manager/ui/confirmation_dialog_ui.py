# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/confirmation_dialog.ui
Classe : Ui_ConfirmationDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_ConfirmationDialog(object):
    def setupUi(self, ConfirmationDialog):
        ConfirmationDialog.setObjectName("ConfirmationDialog")
        ConfirmationDialog.resize(340, 120)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfirmationDialog)
        self.labelMessage = QtWidgets.QLabel(ConfirmationDialog)
        self.labelMessage.setText("Confirmer l'action ?")
        self.labelMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelMessage)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfirmationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)