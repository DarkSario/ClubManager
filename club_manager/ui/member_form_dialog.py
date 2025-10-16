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

class MemberFormDialog(QtWidgets.QDialog, Ui_MemberFormDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Connexions logiques live :
        self.checkMultiClub.toggled.connect(self.toggle_multi_club_fields)
        self.checkMJCElsewhere.toggled.connect(self.toggle_mjc_elsewhere_fields)

    def toggle_multi_club_fields(self, checked):
        self.editExternalClub.setEnabled(checked)
        if not checked:
            self.editExternalClub.clear()

    def toggle_mjc_elsewhere_fields(self, checked):
        self.editMJCClub.setEnabled(checked)
        if not checked:
            self.editMJCClub.clear()

    def accept(self):
        # TODO: validation des champs, RGPD, etc.
        super().accept()