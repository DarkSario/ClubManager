# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/tutorial_dialog.py
Rôle : Fenêtre modale Tutoriel interactif embarqué, navigation pas-à-pas.
Hérite de QDialog et Ui_TutorialDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_TutorialDialog généré par pyuic5 à partir de resources/ui/tutorial_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.tutorial_dialog_ui import Ui_TutorialDialog

class TutorialDialog(QtWidgets.QDialog, Ui_TutorialDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonNext.clicked.connect(self.next_step)
        self.buttonPrev.clicked.connect(self.prev_step)
        self.buttonClose.clicked.connect(self.reject)
        self.steps = [
            "Bienvenue dans Club Manager !\n\nCe tutoriel vous guidera pour la prise en main.",
            "1. Onglet Membres : ajoutez, modifiez, recherchez vos adhérents.",
            "2. Onglet Postes : gérez les rôles (président, trésorier, staff...).",
            "3. Onglet Sessions : créez vos saisons/périodes.",
            "4. Onglet Cotisations : suivez paiements, relances, historiques.",
            "5. Champs personnalisés : ajoutez des informations spécifiques.",
            "6. Exports, Mailing, Sauvegarde, Audit... : tout est accessible en 1 clic !",
            "N'hésitez pas à consulter la documentation pour plus de détails."
        ]
        self.current_step = 0
        self.refresh_step()

    def refresh_step(self):
        self.labelStep.setText(self.steps[self.current_step])
        self.buttonPrev.setEnabled(self.current_step > 0)
        self.buttonNext.setEnabled(self.current_step < len(self.steps)-1)

    def next_step(self):
        if self.current_step < len(self.steps)-1:
            self.current_step += 1
            self.refresh_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.refresh_step()