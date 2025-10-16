# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/backup_restore_dialog.ui
Classe : Ui_BackupRestoreDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_BackupRestoreDialog(object):
    def setupUi(self, BackupRestoreDialog):
        BackupRestoreDialog.setObjectName("BackupRestoreDialog")
        BackupRestoreDialog.resize(420, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(BackupRestoreDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.editBackupPath = QtWidgets.QLineEdit(BackupRestoreDialog)
        self.formLayout.addRow("Chemin du fichier de sauvegarde :", self.editBackupPath)
        self.buttonBrowse = QtWidgets.QPushButton(BackupRestoreDialog)
        self.buttonBrowse.setText("Parcourir...")
        self.formLayout.addRow(self.buttonBrowse)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(BackupRestoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)