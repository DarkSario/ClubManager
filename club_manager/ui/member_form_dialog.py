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
        self.comboPaymentType.currentIndexChanged.connect(self.toggle_payment_type_fields)
        
        # Connexions pour calculer automatiquement le total payé
        self.editCashAmount.textChanged.connect(self.calculate_total_paid)
        self.editCheck1Amount.textChanged.connect(self.calculate_total_paid)
        self.editCheck2Amount.textChanged.connect(self.calculate_total_paid)
        self.editCheck3Amount.textChanged.connect(self.calculate_total_paid)
        
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

    def toggle_payment_type_fields(self, index):
        """Active/désactive le champ club MJC selon le type de paiement."""
        # index 0 = "Club + MJC", index 1 = "Club uniquement (MJC réglée ailleurs)"
        self.comboMJCClub.setEnabled(index == 1)
        if index == 0:
            self.comboMJCClub.setCurrentIndex(0)  # Réinitialiser à "-- Sélectionner --"
    
    def calculate_total_paid(self):
        """Calcule automatiquement le total payé à partir des montants saisis."""
        try:
            cash = float(self.editCashAmount.text() or 0)
        except ValueError:
            cash = 0
        
        try:
            check1 = float(self.editCheck1Amount.text() or 0)
        except ValueError:
            check1 = 0
        
        try:
            check2 = float(self.editCheck2Amount.text() or 0)
        except ValueError:
            check2 = 0
        
        try:
            check3 = float(self.editCheck3Amount.text() or 0)
        except ValueError:
            check3 = 0
        
        total = cash + check1 + check2 + check3
        self.editTotalPaid.setText(f"{total:.2f}")

    def accept(self):
        # Validation des champs obligatoires
        if not self.editLastName.text().strip():
            QtWidgets.QMessageBox.warning(self, "Champ requis", "Le nom est obligatoire.")
            return
        
        if not self.editFirstName.text().strip():
            QtWidgets.QMessageBox.warning(self, "Champ requis", "Le prénom est obligatoire.")
            return
        
        if not self.checkRGPD.isChecked():
            QtWidgets.QMessageBox.warning(self, "RGPD", "Le consentement RGPD est obligatoire.")
            return
        
        # Validation des montants
        try:
            if self.editCashAmount.text().strip():
                float(self.editCashAmount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Le montant en espèce doit être un nombre valide.")
            return
        
        try:
            if self.editCheck1Amount.text().strip():
                float(self.editCheck1Amount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Le montant du chèque 1 doit être un nombre valide.")
            return
        
        try:
            if self.editCheck2Amount.text().strip():
                float(self.editCheck2Amount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Le montant du chèque 2 doit être un nombre valide.")
            return
        
        try:
            if self.editCheck3Amount.text().strip():
                float(self.editCheck3Amount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Le montant du chèque 3 doit être un nombre valide.")
            return
        
        try:
            if self.editANCVAmount.text().strip():
                float(self.editANCVAmount.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Montant invalide", "Le montant ANCV doit être un nombre valide.")
            return
        
        super().accept()