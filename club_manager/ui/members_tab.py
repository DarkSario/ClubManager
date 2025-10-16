# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/members_tab.py
Rôle : Onglet gestion des adhérents (MembersTab) du Club Manager.
Hérite de QWidget et de Ui_MembersTab.
Tous les boutons/actions sont connectés à des slots effectifs dans la classe.
Dépendances : PyQt5, Ui_MembersTab généré par pyuic5 à partir de resources/ui/members_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.members_tab_ui import Ui_MembersTab

class MembersTab(QtWidgets.QWidget, Ui_MembersTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Connexion des boutons du tab à leur logique
        self.buttonAddMember.clicked.connect(self.add_member)
        self.buttonEditMember.clicked.connect(self.edit_member)
        self.buttonDeleteMember.clicked.connect(self.delete_member)
        self.buttonExportMembers.clicked.connect(self.export_members)
        self.buttonFilter.clicked.connect(self.filter_members)
        self.buttonResetFilter.clicked.connect(self.reset_filter)
        self.buttonMailing.clicked.connect(self.do_mailing)
        self.tableMembers.doubleClicked.connect(self.edit_member)
        # TODO : Connexions additionnelles selon les besoins

    def add_member(self):
        # Logique d'ajout d'un adhérent (ouvre le dialog)
        from club_manager.ui.member_form_dialog import MemberFormDialog
        from club_manager.core.members import add_member as add_member_db
        dlg = MemberFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Récupérer toutes les valeurs du formulaire
            try:
                add_member_db(
                    last_name=dlg.editLastName.text(),
                    first_name=dlg.editFirstName.text(),
                    address=dlg.editAddress.text(),
                    postal_code=dlg.editPostalCode.text(),
                    city=dlg.editCity.text(),
                    phone=dlg.editPhone.text(),
                    mail=dlg.editMail.text(),
                    rgpd=int(dlg.checkRGPD.isChecked()),
                    image_rights=int(dlg.checkImageRights.isChecked()),
                    health=dlg.editHealth.text(),
                    ancv=int(dlg.checkANCV.isChecked()),
                    cash=float(dlg.editCash.text() or '0'),
                    cheque1=dlg.editCheque1.text(),
                    cheque2=dlg.editCheque2.text(),
                    cheque3=dlg.editCheque3.text(),
                    total_paid=float(dlg.editTotalPaid.text() or '0'),
                    club_part=float(dlg.editClubPart.text() or '0'),
                    mjc_part=float(dlg.editMJCPart.text() or '0'),
                    external_club=dlg.editExternalClub.text() if dlg.checkMultiClub.isChecked() else None,
                    mjc_elsewhere=dlg.editMJCClub.text() if dlg.checkMJCElsewhere.isChecked() else None
                )
                # Recharger la table
                self.refresh_members()
                QtWidgets.QMessageBox.information(self, "Succès", "Membre ajouté avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du membre : {str(e)}")
    
    def edit_member(self):
        # Logique de modification d'un adhérent sélectionné
        # TODO: Récupérer l'ID du membre sélectionné
        pass

    def delete_member(self):
        # Logique de suppression d'un ou plusieurs membres sélectionnés
        pass

    def export_members(self):
        # Logique d'export CSV/PDF de la liste actuelle
        pass

    def filter_members(self):
        # Logique de filtrage multicritère
        pass

    def reset_filter(self):
        # Réinitialise tous les filtres
        pass

    def do_mailing(self):
        # Lancer le module de mailing sur sélection
        pass

    def refresh_members(self):
        # Recharge la table depuis la base
        from club_manager.core.members import get_all_members
        members = get_all_members()
        self.tableMembers.setRowCount(0)
        for row_idx, member in enumerate(members):
            self.tableMembers.insertRow(row_idx)
            self.tableMembers.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(member['last_name'] or '')))
            self.tableMembers.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(member['first_name'] or '')))
            self.tableMembers.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(member['address'] or '')))
            self.tableMembers.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(member['postal_code'] or '')))
            self.tableMembers.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(member['city'] or '')))
            self.tableMembers.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(str(member['phone'] or '')))
            self.tableMembers.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(member['mail'] or '')))
            self.tableMembers.setItem(row_idx, 7, QtWidgets.QTableWidgetItem('Oui' if member['rgpd'] else 'Non'))
            self.tableMembers.setItem(row_idx, 8, QtWidgets.QTableWidgetItem('Oui' if member['image_rights'] else 'Non'))
            self.tableMembers.setItem(row_idx, 9, QtWidgets.QTableWidgetItem(str(member['total_paid'] or '0')))
            # Stocker l'ID du membre dans la première colonne
            self.tableMembers.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, member['id'])