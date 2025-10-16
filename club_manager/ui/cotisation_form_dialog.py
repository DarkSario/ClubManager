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
    self.buttonBox.accepted.connect(self.accept)
    self.buttonBox.rejected.connect(self.reject)
    self.comboMethod.currentTextChanged.connect(self.method_changed)
    try:
        self.editChequeNumber.hide()
    except Exception:
        pass


    
def accept(self):
    # Validation du montant payé
    try:
        amount = float(self.editPaid.text())
    except ValueError:
        QtWidgets.QMessageBox.warning(self, "Erreur", "Le montant payé doit être un nombre.")
        return
    if self.comboMethod.currentText() == "Chèque":
        try:
            if not self.editChequeNumber.text():
                QtWidgets.QMessageBox.warning(self, "Erreur", "Le numéro de chèque est obligatoire.")
                return
        except Exception:
            pass
    # autres validations ici...
    super().accept()

    def method_changed(self, method):
        try:
            if method == "Chèque":
                self.editChequeNumber.show()
            else:
                self.editChequeNumber.hide()
                self.editChequeNumber.clear()
        except Exception:
            pass
