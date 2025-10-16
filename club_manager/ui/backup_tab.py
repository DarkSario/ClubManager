# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/backup_tab.py
Rôle : Onglet sauvegarde/restauration (BackupTab) du Club Manager.
Hérite de QWidget et de Ui_BackupTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_BackupTab généré par pyuic5 à partir de resources/ui/backup_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.backup_tab_ui import Ui_BackupTab
from club_manager.core.backup import backup_database, restore_database, export_zip_archive, import_zip_archive

class BackupTab(QtWidgets.QWidget, Ui_BackupTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBackup.clicked.connect(self.start_backup)
        self.buttonRestore.clicked.connect(self.start_restore)
        self.buttonExportZip.clicked.connect(self.start_export_zip)
        self.buttonImportZip.clicked.connect(self.start_import_zip)

    def start_backup(self):
        # Sauvegarde manuelle de la base
        backup_database("club_manager.db", parent=self)

    def start_restore(self):
        # Restauration d'une sauvegarde
        restore_database(parent=self)

    def start_export_zip(self):
        # Export complet (archive zip)
        export_zip_archive(parent=self)

    def start_import_zip(self):
        # Import complet (archive zip)
        import_zip_archive(parent=self)