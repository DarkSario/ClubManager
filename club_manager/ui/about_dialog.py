# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/about_dialog.py
Rôle : Fenêtre modale "À propos" (version, crédits, informations légales).
Hérite de QDialog et Ui_AboutDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_AboutDialog généré par pyuic5 à partir de resources/ui/about_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.about_dialog_ui import Ui_AboutDialog

class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)