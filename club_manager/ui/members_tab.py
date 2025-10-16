# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/members_tab.py
Rôle : Onglet gestion des adhérents (MembersTab) du Club Manager.
Hérite de QWidget et de Ui_MembersTab.
Tous les boutons/actions sont connectés à des slots effectifs dans la classe.
Dépendances : PyQt5, Ui_MembersTab généré par pyuic5 à partir de resources/ui/members_tab.ui
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from club_manager.ui.members_tab_ui import Ui_MembersTab
from club_manager.ui.confirmation_dialog import ConfirmationDialog
import csv
import os

class MembersTab(QtWidgets.QWidget, Ui_MembersTab):
    """Onglet de gestion des membres avec CRUD complet et export."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._current_filter = {}
        
        # Connexion des boutons du tab à leur logique
        self.buttonAddMember.clicked.connect(self.add_member)
        self.buttonEditMember.clicked.connect(self.edit_member)
        self.buttonDeleteMember.clicked.connect(self.delete_member)
        self.buttonExportMembers.clicked.connect(self.export_members)
        self.buttonFilter.clicked.connect(self.filter_members)
        self.buttonResetFilter.clicked.connect(self.reset_filter)
        self.buttonMailing.clicked.connect(self.do_mailing)
        self.tableMembers.doubleClicked.connect(self.edit_member)
        
        # Charger les membres au démarrage
        try:
            self.refresh_members()
        except:
            pass  # La base n'est peut-être pas encore initialisée

    def add_member(self):
        """Ajoute un nouveau membre après validation."""
        from club_manager.ui.member_form_dialog import MemberFormDialog
        from club_manager.core.members import add_member as add_member_db
        
        dlg = MemberFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Validation des champs obligatoires
            if not dlg.editLastName.text() or not dlg.editFirstName.text():
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Champs obligatoires", 
                    "Le nom et le prénom sont obligatoires."
                )
                return
            
            if not dlg.checkRGPD.isChecked():
                QtWidgets.QMessageBox.warning(
                    self,
                    "RGPD requis",
                    "Le consentement RGPD est obligatoire pour enregistrer un membre."
                )
                return
            
            try:
                # Récupérer le type de paiement
                payment_type = "club_mjc" if dlg.comboPaymentType.currentIndex() == 0 else "club_only"
                
                # Récupérer l'ID du club MJC si applicable
                mjc_club_id = None
                if payment_type == "club_only" and dlg.comboMJCClub.currentIndex() > 0:
                    mjc_club_id = dlg.comboMJCClub.currentData()
                
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
                    payment_type=payment_type,
                    ancv_amount=float(dlg.editANCVAmount.text() or '0'),
                    mjc_club_id=mjc_club_id,
                    cotisation_status=dlg.comboCotisationStatus.currentText(),
                    external_club=dlg.editExternalClub.text() if dlg.checkMultiClub.isChecked() else None
                )
                self.refresh_members()
                QtWidgets.QMessageBox.information(self, "Succès", "Membre ajouté avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du membre : {str(e)}")
    
    def edit_member(self):
        """Édite le membre sélectionné."""
        from club_manager.ui.member_form_dialog import MemberFormDialog
        from club_manager.core.members import get_member_by_id, update_member
        
        selected_items = self.tableMembers.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un membre à modifier.")
            return
        
        # Récupérer l'ID du membre depuis la première colonne
        row = selected_items[0].row()
        member_id = self.tableMembers.item(row, 0).data(Qt.UserRole)
        
        if not member_id:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de récupérer l'ID du membre.")
            return
        
        try:
            member = get_member_by_id(member_id)
            if not member:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Membre introuvable.")
                return
            
            # Pré-remplir le formulaire
            dlg = MemberFormDialog(self)
            dlg.setWindowTitle("Modifier un membre")
            dlg.editLastName.setText(member.get('last_name', ''))
            dlg.editFirstName.setText(member.get('first_name', ''))
            dlg.editAddress.setText(member.get('address', ''))
            dlg.editPostalCode.setText(member.get('postal_code', ''))
            dlg.editCity.setText(member.get('city', ''))
            dlg.editPhone.setText(member.get('phone', ''))
            dlg.editMail.setText(member.get('mail', ''))
            dlg.checkRGPD.setChecked(bool(member.get('rgpd', 0)))
            dlg.checkImageRights.setChecked(bool(member.get('image_rights', 0)))
            dlg.editHealth.setText(member.get('health', ''))
            
            # Restaurer le type de paiement
            payment_type = member.get('payment_type', 'club_mjc')
            if payment_type == 'club_only':
                dlg.comboPaymentType.setCurrentIndex(1)
                # Restaurer le club MJC sélectionné
                mjc_club_id = member.get('mjc_club_id')
                if mjc_club_id:
                    for i in range(dlg.comboMJCClub.count()):
                        if dlg.comboMJCClub.itemData(i) == mjc_club_id:
                            dlg.comboMJCClub.setCurrentIndex(i)
                            break
            else:
                dlg.comboPaymentType.setCurrentIndex(0)
            
            dlg.editANCVAmount.setText(str(member.get('ancv_amount', 0)))
            
            # Restaurer le statut de cotisation
            status = member.get('cotisation_status', 'Non payée')
            index = dlg.comboCotisationStatus.findText(status)
            if index >= 0:
                dlg.comboCotisationStatus.setCurrentIndex(index)
            
            if member.get('external_club'):
                dlg.checkMultiClub.setChecked(True)
                dlg.editExternalClub.setText(member.get('external_club', ''))
            
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                # Validation
                if not dlg.editLastName.text() or not dlg.editFirstName.text():
                    QtWidgets.QMessageBox.warning(self, "Champs obligatoires", "Le nom et le prénom sont obligatoires.")
                    return
                
                # Récupérer le type de paiement
                payment_type = "club_mjc" if dlg.comboPaymentType.currentIndex() == 0 else "club_only"
                
                # Récupérer l'ID du club MJC si applicable
                mjc_club_id = None
                if payment_type == "club_only" and dlg.comboMJCClub.currentIndex() > 0:
                    mjc_club_id = dlg.comboMJCClub.currentData()
                
                update_member(
                    member_id,
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
                    payment_type=payment_type,
                    ancv_amount=float(dlg.editANCVAmount.text() or '0'),
                    mjc_club_id=mjc_club_id,
                    cotisation_status=dlg.comboCotisationStatus.currentText(),
                    external_club=dlg.editExternalClub.text() if dlg.checkMultiClub.isChecked() else None
                )
                self.refresh_members()
                QtWidgets.QMessageBox.information(self, "Succès", "Membre modifié avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")

    def delete_member(self):
        """Supprime le(s) membre(s) sélectionné(s) après confirmation."""
        from club_manager.core.members import delete_member as delete_member_db
        
        selected_items = self.tableMembers.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un ou plusieurs membres à supprimer.")
            return
        
        # Récupérer les lignes uniques sélectionnées
        selected_rows = set(item.row() for item in selected_items)
        member_count = len(selected_rows)
        
        # Demander confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer {member_count} membre(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    member_id = self.tableMembers.item(row, 0).data(Qt.UserRole)
                    if member_id:
                        delete_member_db(member_id)
                
                self.refresh_members()
                QtWidgets.QMessageBox.information(self, "Succès", f"{member_count} membre(s) supprimé(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_members(self):
        """Exporte la liste des membres en CSV."""
        from club_manager.core.members import get_all_members
        
        # Demander le chemin de sauvegarde
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Exporter les membres",
            os.path.expanduser("~/membres_export.csv"),
            "Fichiers CSV (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            members = get_all_members()
            if not members:
                QtWidgets.QMessageBox.information(self, "Export", "Aucun membre à exporter.")
                return
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = members[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(members)
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{len(members)} membre(s) exporté(s) vers :\n{file_path}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export : {str(e)}")

    def filter_members(self):
        """Filtre les membres selon les critères saisis."""
        # TODO: Implémenter le filtrage avec les widgets de filtres disponibles
        QtWidgets.QMessageBox.information(
            self,
            "Filtre",
            "La fonctionnalité de filtrage sera implémentée prochainement."
        )

    def reset_filter(self):
        """Réinitialise tous les filtres et recharge tous les membres."""
        self._current_filter = {}
        self.refresh_members()

    def do_mailing(self):
        """Lance le module de mailing pour les membres sélectionnés."""
        selected_items = self.tableMembers.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner au moins un membre pour le mailing."
            )
            return
        
        QtWidgets.QMessageBox.information(
            self,
            "Mailing",
            "La fonctionnalité de mailing sera implémentée via l'onglet Mailing."
        )

    def refresh_members(self):
        """Recharge la table des membres depuis la base de données."""
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
            # Stocker l'ID du membre dans la première colonne avec Qt.UserRole
            self.tableMembers.item(row_idx, 0).setData(Qt.UserRole, member['id'])