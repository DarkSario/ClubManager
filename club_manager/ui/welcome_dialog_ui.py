# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/welcome_dialog.ui
Classe : Ui_WelcomeDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_WelcomeDialog(object):
    def setupUi(self, WelcomeDialog):
        WelcomeDialog.setObjectName("WelcomeDialog")
        WelcomeDialog.resize(500, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(WelcomeDialog)
        self.labelLogo = QtWidgets.QLabel(WelcomeDialog)
        self.labelLogo.setText("CLUB MANAGER")
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelLogo)
        self.labelDesc = QtWidgets.QLabel(WelcomeDialog)
        self.labelDesc.setText("Bienvenue ! Choisissez une base existante ou créez-en une nouvelle.\nAccédez au tutoriel ou à la documentation à tout moment.")
        self.labelDesc.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelDesc)
        self.formLayout = QtWidgets.QFormLayout()
        self.editDBPath = QtWidgets.QLineEdit(WelcomeDialog)
        self.formLayout.addRow("Base de données :", self.editDBPath)
        self.buttonOpenDB = QtWidgets.QPushButton(WelcomeDialog)
        self.buttonOpenDB.setText("Ouvrir une base existante")
        self.buttonNewDB = QtWidgets.QPushButton(WelcomeDialog)
        self.buttonNewDB.setText("Créer une nouvelle base")
        self.formLayout.addRow(self.buttonOpenDB, self.buttonNewDB)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.buttonTutorial = QtWidgets.QPushButton(WelcomeDialog)
        self.buttonTutorial.setText("Tutoriel interactif")
        self.buttonDoc = QtWidgets.QPushButton(WelcomeDialog)
        self.buttonDoc.setText("Documentation")
        self.horizontalLayout.addWidget(self.buttonTutorial)
        self.horizontalLayout.addWidget(self.buttonDoc)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(WelcomeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)