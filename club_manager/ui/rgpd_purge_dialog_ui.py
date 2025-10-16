# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/rgpd_purge_dialog.ui
Classe : Ui_RgpdPurgeDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_RgpdPurgeDialog(object):
    def setupUi(self, RgpdPurgeDialog):
        RgpdPurgeDialog.setObjectName("RgpdPurgeDialog")
        RgpdPurgeDialog.resize(420, 180)
        self.verticalLayout = QtWidgets.QVBoxLayout(RgpdPurgeDialog)
        self.labelWarning = QtWidgets.QLabel(RgpdPurgeDialog)
        self.labelWarning.setText(
            "<b>Attention !</b><br>Cet outil lance une purge/anonymisation RGPD irréversible.<br>Êtes-vous sûr de vouloir continuer ?"
        )
        self.labelWarning.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWarning.setWordWrap(True)
        self.verticalLayout.addWidget(self.labelWarning)
        self.checkUnderstand = QtWidgets.QCheckBox(RgpdPurgeDialog)
        self.checkUnderstand.setText("J'ai compris les conséquences de cette action.")
        self.verticalLayout.addWidget(self.checkUnderstand)
        self.buttonBox = QtWidgets.QDialogButtonBox(RgpdPurgeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)