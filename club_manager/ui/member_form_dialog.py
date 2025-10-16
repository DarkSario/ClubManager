# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/member_form_dialog.py
Rôle : Fenêtre modale d'ajout/édition d'adhérent.
Hérite de QDialog et Ui_MemberFormDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_MemberFormDialog généré par pyuic5 à partir de resources/ui/member_form_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.member_form_dialog_ui import Ui_MemberFormDialog
from club_manager.core.mjc_clubs import get_all_mjc_clubs

class MemberFormDialog(QtWidgets.QDialog, Ui_MemberFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Connexions logiques live :
        self.checkMultiClub.toggled.connect(self.toggle_multi_club_fields)
        self.comboPaymentType.currentIndexChanged.connect(self.toggle_payment_type_fields)
        
        # Charger les clubs MJC
        self.load_mjc_clubs()
    
    def load_mjc_clubs(self):
        """Charge la liste des clubs MJC dans le combobox."""
        try:
            clubs = get_all_mjc_clubs()
            self.comboMJCClub.clear()
            self.comboMJCClub.addItem("-- Sélectionner un club MJC --", None)
            for club in clubs:
                self.comboMJCClub.addItem(club['name'], club['id'])
        except:
            pass  # La base n'est peut-être pas encore initialisée

    def toggle_multi_club_fields(self, checked):
        self.editExternalClub.setEnabled(checked)
        if not checked:
            self.editExternalClub.clear()
    
    def toggle_payment_type_fields(self, index):
        """Active/désactive le champ club MJC selon le type de paiement."""
        # index 0 = "Club + MJC", index 1 = "Club uniquement (MJC réglée ailleurs)"
        self.comboMJCClub.setEnabled(index == 1)
        if index == 0:
            self.comboMJCClub.setCurrentIndex(0)  # Réinitialiser à "-- Sélectionner --"

    def accept(self):
        # TODO: validation des champs, RGPD, etc.
        super().accept()