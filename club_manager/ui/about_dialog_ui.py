# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/about_dialog.ui
Classe : Ui_AboutDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(400, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.labelLogo = QtWidgets.QLabel(AboutDialog)
        self.labelLogo.setText("CLUB MANAGER")
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelLogo)
        self.labelVersion = QtWidgets.QLabel(AboutDialog)
        self.labelVersion.setText("Version 1.0.0")
        self.labelVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelVersion)
        self.labelCopyright = QtWidgets.QLabel(AboutDialog)
        self.labelCopyright.setText("© 2025 DarkSario\nLicence libre, voir documentation.")
        self.labelCopyright.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelCopyright)
        self.textCredits = QtWidgets.QTextBrowser(AboutDialog)
        self.textCredits.setHtml(
            "<b>Auteurs</b>: DarkSario & contributeurs<br>"
            "<b>Remerciements</b>: Projet open-source inspiré par la communauté.<br>"
            "<b>Librairies</b>: PyQt5, SQLite, etc.<br><br>"
            "<i>Pour toute remarque ou bug, voir la documentation ou le dépôt GitHub.</i>"
        )
        self.textCredits.setOpenExternalLinks(True)
        self.verticalLayout.addWidget(self.textCredits)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)