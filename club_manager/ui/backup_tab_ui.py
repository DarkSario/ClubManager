# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/backup_tab.ui
Classe : Ui_BackupTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_BackupTab(object):
    def setupUi(self, BackupTab):
        BackupTab.setObjectName("BackupTab")
        BackupTab.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(BackupTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonBackup = QtWidgets.QPushButton(BackupTab)
        self.buttonBackup.setText("Sauvegarder")
        self.buttonRestore = QtWidgets.QPushButton(BackupTab)
        self.buttonRestore.setText("Restaurer")
        self.buttonExportZip = QtWidgets.QPushButton(BackupTab)
        self.buttonExportZip.setText("Exporter (zip)")
        self.buttonImportZip = QtWidgets.QPushButton(BackupTab)
        self.buttonImportZip.setText("Importer (zip)")
        self.horizontalLayoutTop.addWidget(self.buttonBackup)
        self.horizontalLayoutTop.addWidget(self.buttonRestore)
        self.horizontalLayoutTop.addWidget(self.buttonExportZip)
        self.horizontalLayoutTop.addWidget(self.buttonImportZip)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.labelLastBackup = QtWidgets.QLabel(BackupTab)
        self.labelLastBackup.setText("Dernière sauvegarde : inconnue")
        self.verticalLayout.addWidget(self.labelLastBackup)