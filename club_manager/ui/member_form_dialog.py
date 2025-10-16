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
    def __init__(self, parent=None, member=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Connexions logiques live :
        self.checkMultiClub.toggled.connect(self.toggle_multi_club_fields)
        self.checkMJCElsewhere.toggled.connect(self.toggle_mjc_elsewhere_fields)
        
        # Si un membre est fourni, pré-remplir les champs
        if member:
            self.populate_form(member)

    def toggle_multi_club_fields(self, checked):
        self.editExternalClub.setEnabled(checked)
        if not checked:
            self.editExternalClub.clear()

    def toggle_mjc_elsewhere_fields(self, checked):
        self.editMJCClub.setEnabled(checked)
        if not checked:
            self.editMJCClub.clear()

    def populate_form(self, member):
        """Remplit le formulaire avec les données d'un membre existant."""
        self.editLastName.setText(str(member['last_name'] or ''))
        self.editFirstName.setText(str(member['first_name'] or ''))
        self.editAddress.setText(str(member['address'] or ''))
        self.editPostalCode.setText(str(member['postal_code'] or ''))
        self.editCity.setText(str(member['city'] or ''))
        self.editPhone.setText(str(member['phone'] or ''))
        self.editMail.setText(str(member['mail'] or ''))
        self.checkRGPD.setChecked(bool(member['rgpd']))
        self.checkImageRights.setChecked(bool(member['image_rights']))
        self.editHealth.setText(str(member['health'] or ''))
        self.checkANCV.setChecked(bool(member['ancv']))
        self.editCash.setText(str(member['cash'] or '0'))
        self.editCheque1.setText(str(member['cheque1'] or ''))
        self.editCheque2.setText(str(member['cheque2'] or ''))
        self.editCheque3.setText(str(member['cheque3'] or ''))
        self.editTotalPaid.setText(str(member['total_paid'] or '0'))
        self.editClubPart.setText(str(member['club_part'] or '0'))
        self.editMJCPart.setText(str(member['mjc_part'] or '0'))
        
        if member.get('external_club'):
            self.checkMultiClub.setChecked(True)
            self.editExternalClub.setText(str(member['external_club']))
        
        if member.get('mjc_elsewhere'):
            self.checkMJCElsewhere.setChecked(True)
            self.editMJCClub.setText(str(member['mjc_elsewhere']))
    
    def accept(self):
        # TODO: validation des champs, RGPD, etc.
        super().accept()