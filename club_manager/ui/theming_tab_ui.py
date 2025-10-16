# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/theming_tab.ui
Classe : Ui_ThemingTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_ThemingTab(object):
    def setupUi(self, ThemingTab):
        ThemingTab.setObjectName("ThemingTab")
        ThemingTab.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(ThemingTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonChooseTheme = QtWidgets.QPushButton(ThemingTab)
        self.buttonChooseTheme.setText("Choisir un thème")
        self.buttonImportLogo = QtWidgets.QPushButton(ThemingTab)
        self.buttonImportLogo.setText("Importer un logo")
        self.buttonPreviewTheme = QtWidgets.QPushButton(ThemingTab)
        self.buttonPreviewTheme.setText("Prévisualiser")
        self.horizontalLayoutTop.addWidget(self.buttonChooseTheme)
        self.horizontalLayoutTop.addWidget(self.buttonImportLogo)
        self.horizontalLayoutTop.addWidget(self.buttonPreviewTheme)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.labelPreview = QtWidgets.QLabel(ThemingTab)
        self.labelPreview.setText("Aperçu du thème ici")
        self.labelPreview.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelPreview)