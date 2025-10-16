# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/audit_details_dialog.py
Rôle : Fenêtre modale de détails d'une entrée d'audit.
Hérite de QDialog et Ui_AuditDetailsDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_AuditDetailsDialog généré par pyuic5 à partir de resources/ui/audit_details_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.audit_details_dialog_ui import Ui_AuditDetailsDialog

class AuditDetailsDialog(QtWidgets.QDialog, Ui_AuditDetailsDialog):
    def __init__(self, parent=None, details=None):
        super().__init__(parent)
        self.setupUi(self)
        if details:
            self.labelDate.setText(details.get("date", ""))
            self.labelAction.setText(details.get("action", ""))
            self.labelUser.setText(details.get("user", ""))
            self.labelObject.setText(details.get("object", ""))
            self.textDetails.setPlainText(details.get("details", ""))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)