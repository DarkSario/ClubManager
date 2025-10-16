# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/welcome_dialog.py
Rôle : Fenêtre d'accueil au lancement (choix base, création nouvelle base, accès tutoriel/doc).
Hérite de QDialog et Ui_WelcomeDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_WelcomeDialog généré par pyuic5 à partir de resources/ui/welcome_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.welcome_dialog_ui import Ui_WelcomeDialog

class WelcomeDialog(QtWidgets.QDialog, Ui_WelcomeDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonOpenDB.clicked.connect(self.open_db)
        self.buttonNewDB.clicked.connect(self.create_db)
        self.buttonTutorial.clicked.connect(self.open_tutorial)
        self.buttonDoc.clicked.connect(self.open_doc)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def open_db(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Ouvrir une base existante", "", "Fichiers Club (*.db);;Tous les fichiers (*)")
        if fname:
            self.editDBPath.setText(fname)

    def create_db(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Créer une nouvelle base", "", "Fichiers Club (*.db);;Tous les fichiers (*)")
        if fname:
            self.editDBPath.setText(fname)

    def open_tutorial(self):
        QtWidgets.QMessageBox.information(self, "Tutoriel", "Lancement du tutoriel interactif... (fonctionnalité à compléter)")

    def open_doc(self):
        QtWidgets.QMessageBox.information(self, "Documentation", "Ouverture de la documentation utilisateur...")