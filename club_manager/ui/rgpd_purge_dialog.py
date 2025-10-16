# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/rgpd_purge_dialog.py
Rôle : Fenêtre modale pour lancer/valider la purge RGPD.
Hérite de QDialog et Ui_RgpdPurgeDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_RgpdPurgeDialog généré par pyuic5 à partir de resources/ui/rgpd_purge_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.rgpd_purge_dialog_ui import Ui_RgpdPurgeDialog

class RgpdPurgeDialog(QtWidgets.QDialog, Ui_RgpdPurgeDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)