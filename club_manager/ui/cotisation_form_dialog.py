# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/cotisation_form_dialog.py
Rôle : Fenêtre modale d'ajout/édition de cotisation.
Hérite de QDialog et Ui_CotisationFormDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CotisationFormDialog généré par pyuic5 à partir de resources/ui/cotisation_form_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.cotisation_form_dialog_ui import Ui_CotisationFormDialog

class CotisationFormDialog(QtWidgets.QDialog, Ui_CotisationFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept_with_validation)
        self.buttonBox.rejected.connect(self.reject)
        self.comboMethod.currentTextChanged.connect(self.method_changed)
        # Cacher le champ numéro de chèque par défaut
        self.editChequeNumber.hide()
        # Trouver le label du numéro de chèque et le cacher aussi
        for i in range(self.formLayout.rowCount()):
            label_item = self.formLayout.itemAt(i, QtWidgets.QFormLayout.LabelRole)
            if label_item and label_item.widget() and label_item.widget().text() == "Numéro de chèque :":
                label_item.widget().hide()
                self.cheque_label = label_item.widget()
                break
        else:
            self.cheque_label = None
    
    def accept_with_validation(self):
        """Valide les données avant d'accepter le dialogue."""
        # Validation du montant
        try:
            amount = float(self.editAmount.text() or '0')
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le montant doit être un nombre valide.")
            return
        
        # Validation du montant payé
        try:
            paid = float(self.editPaid.text() or '0')
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le montant payé doit être un nombre valide.")
            return
        
        # Validation du numéro de chèque si la méthode est "Chèque"
        if self.comboMethod.currentText() == "Chèque":
            if not self.editChequeNumber.text().strip():
                QtWidgets.QMessageBox.warning(self, "Erreur", "Le numéro de chèque est obligatoire pour un paiement par chèque.")
                return
        
        # Toutes les validations sont passées
        self.accept()
    
    def method_changed(self, method):
        """Affiche ou cache le champ numéro de chèque selon la méthode."""
        if method == "Chèque":
            self.editChequeNumber.show()
            if self.cheque_label:
                self.cheque_label.show()
        else:
            self.editChequeNumber.hide()
            if self.cheque_label:
                self.cheque_label.hide()
            self.editChequeNumber.clear()

