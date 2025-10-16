# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/error_dialog.ui
Classe : Ui_ErrorDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog):
        ErrorDialog.setObjectName("ErrorDialog")
        ErrorDialog.resize(420, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(ErrorDialog)
        self.labelError = QtWidgets.QLabel(ErrorDialog)
        self.labelError.setText("Une erreur est survenue.")
        self.labelError.setAlignment(QtCore.Qt.AlignCenter)
        self.labelError.setWordWrap(True)
        self.verticalLayout.addWidget(self.labelError)
        self.buttonBox = QtWidgets.QDialogButtonBox(ErrorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)