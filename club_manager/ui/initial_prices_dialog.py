# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/initial_prices_dialog.py
Rôle : Dialogue de configuration initiale des tarifs lors de la création d'une nouvelle base.
"""

from PyQt5 import QtWidgets, QtCore
from club_manager.ui.initial_prices_dialog_ui import Ui_InitialPricesDialog
from club_manager.core.annual_prices import add_annual_price
from datetime import datetime

class InitialPricesDialog(QtWidgets.QDialog, Ui_InitialPricesDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Pré-remplir l'année courante
        current_year = datetime.now().year
        self.editYear.setText(f"{current_year}-{current_year + 1}")
        
        # Désactiver le bouton de fermeture pour forcer la configuration
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
    
    def accept(self):
        """Valide et enregistre les tarifs."""
        year = self.editYear.text().strip()
        club_price = self.editClubPrice.text().strip()
        mjc_price = self.editMJCPrice.text().strip()
        
        # Validation
        if not year:
            QtWidgets.QMessageBox.warning(self, "Champ requis", "Veuillez saisir l'année.")
            return
        
        if not club_price:
            QtWidgets.QMessageBox.warning(self, "Champ requis", "Veuillez saisir le prix Club.")
            return
        
        if not mjc_price:
            QtWidgets.QMessageBox.warning(self, "Champ requis", "Veuillez saisir le prix MJC.")
            return
        
        try:
            club_price_float = float(club_price)
            mjc_price_float = float(mjc_price)
            
            if club_price_float < 0 or mjc_price_float < 0:
                QtWidgets.QMessageBox.warning(self, "Montant invalide", "Les prix ne peuvent pas être négatifs.")
                return
            
            # Enregistrer les tarifs comme tarifs courants
            add_annual_price(year, club_price_float, mjc_price_float, is_current=True)
            
            super().accept()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Les prix doivent être des nombres valides.")
    
    def reject(self):
        """Empêche la fermeture sans configuration."""
        reply = QtWidgets.QMessageBox.warning(
            self,
            "Configuration requise",
            "La configuration des tarifs est obligatoire pour utiliser cette base de données.\n"
            "Voulez-vous vraiment annuler ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            super().reject()
