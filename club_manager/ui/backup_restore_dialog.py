# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/backup_restore_dialog.py
Rôle : Fenêtre modale de restauration de sauvegarde.
Hérite de QDialog et Ui_BackupRestoreDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_BackupRestoreDialog généré par pyuic5 à partir de resources/ui/backup_restore_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.backup_restore_dialog_ui import Ui_BackupRestoreDialog

class BackupRestoreDialog(QtWidgets.QDialog, Ui_BackupRestoreDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBrowse.clicked.connect(self.browse_file)

    def browse_file(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Sélectionner une sauvegarde", "", "Fichiers ZIP (*.zip);;Tous les fichiers (*)")
        if fname:
            self.editBackupPath.setText(fname)