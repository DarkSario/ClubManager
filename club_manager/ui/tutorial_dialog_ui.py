# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/tutorial_dialog.ui
Classe : Ui_TutorialDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_TutorialDialog(object):
    def setupUi(self, TutorialDialog):
        TutorialDialog.setObjectName("TutorialDialog")
        TutorialDialog.resize(500, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(TutorialDialog)
        self.labelStep = QtWidgets.QLabel(TutorialDialog)
        self.labelStep.setWordWrap(True)
        self.labelStep.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelStep)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.buttonPrev = QtWidgets.QPushButton(TutorialDialog)
        self.buttonPrev.setText("Précédent")
        self.buttonNext = QtWidgets.QPushButton(TutorialDialog)
        self.buttonNext.setText("Suivant")
        self.buttonClose = QtWidgets.QPushButton(TutorialDialog)
        self.buttonClose.setText("Fermer")
        self.horizontalLayout.addWidget(self.buttonPrev)
        self.horizontalLayout.addWidget(self.buttonNext)
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)