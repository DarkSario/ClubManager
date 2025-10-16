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
        # Charger les membres au démarrage
        try:
            self.refresh_members()
        except:
            pass  # La base n'est peut-être pas encore initialisée

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
        selected_rows = self.tableMembers.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner un membre à modifier.")
            return
        
        # Récupérer l'ID du membre depuis la première colonne
        row = selected_rows[0].row()
        member_id = self.tableMembers.item(row, 0).data(QtWidgets.QTableWidgetItem.UserType)
        
        from club_manager.ui.member_form_dialog import MemberFormDialog
        from club_manager.core.members import get_member_by_id, update_member
        
        # Charger les données du membre
        member = get_member_by_id(member_id)
        if not member:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Membre introuvable.")
            return
        
        # Ouvrir le dialog avec les données pré-remplies
        dlg = MemberFormDialog(self, member)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            try:
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
                QtWidgets.QMessageBox.information(self, "Succès", "Membre modifié avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification du membre : {str(e)}")

    def delete_member(self):
        # Logique de suppression d'un ou plusieurs membres sélectionnés
        selected_rows = self.tableMembers.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un membre à supprimer.")
            return
        
        # Demander confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer {len(selected_rows)} membre(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            from club_manager.core.members import delete_member as delete_member_db
            try:
                for row in selected_rows:
                    member_id = self.tableMembers.item(row.row(), 0).data(QtWidgets.QTableWidgetItem.UserType)
                    delete_member_db(member_id)
                
                # Recharger la table
                self.refresh_members()
                QtWidgets.QMessageBox.information(self, "Succès", f"{len(selected_rows)} membre(s) supprimé(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_members(self):
        # Logique d'export CSV/PDF de la liste actuelle
        from PyQt5.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les membres",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                from club_manager.core.members import get_all_members
                members = get_all_members()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nom', 'Prénom', 'Adresse', 'Code Postal', 'Ville', 'Téléphone', 'Email', 'RGPD', 'Droits Image', 'Total Payé']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for member in members:
                        writer.writerow({
                            'Nom': member['last_name'] or '',
                            'Prénom': member['first_name'] or '',
                            'Adresse': member['address'] or '',
                            'Code Postal': member['postal_code'] or '',
                            'Ville': member['city'] or '',
                            'Téléphone': member['phone'] or '',
                            'Email': member['mail'] or '',
                            'RGPD': 'Oui' if member['rgpd'] else 'Non',
                            'Droits Image': 'Oui' if member['image_rights'] else 'Non',
                            'Total Payé': member['total_paid'] or '0'
                        })
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Export réussi vers {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def filter_members(self):
        # Logique de filtrage multicritère
        # Pour l'instant, un filtre simple par nom
        filter_text, ok = QtWidgets.QInputDialog.getText(
            self,
            "Filtrer les membres",
            "Entrez un nom ou prénom à rechercher:"
        )
        
        if ok and filter_text:
            from club_manager.core.members import get_all_members
            members = get_all_members()
            
            # Filtrer les membres
            filtered_members = [
                m for m in members
                if filter_text.lower() in (m['last_name'] or '').lower()
                or filter_text.lower() in (m['first_name'] or '').lower()
            ]
            
            # Afficher les résultats filtrés
            self.tableMembers.setRowCount(0)
            for row_idx, member in enumerate(filtered_members):
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
                self.tableMembers.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, member['id'])
            
            QtWidgets.QMessageBox.information(self, "Filtre appliqué", f"{len(filtered_members)} membre(s) trouvé(s).")

    def reset_filter(self):
        # Réinitialise tous les filtres
        self.refresh_members()
        QtWidgets.QMessageBox.information(self, "Filtre réinitialisé", "Tous les membres sont à nouveau affichés.")

    def do_mailing(self):
        # Lancer le module de mailing sur sélection
        selected_rows = self.tableMembers.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un membre pour le mailing.")
            return
        
        # Récupérer les emails des membres sélectionnés
        emails = []
        for row in selected_rows:
            email = self.tableMembers.item(row.row(), 6).text()
            if email:
                emails.append(email)
        
        if not emails:
            QtWidgets.QMessageBox.warning(self, "Attention", "Aucun des membres sélectionnés n'a d'adresse email.")
            return
        
        # Afficher les emails sélectionnés
        QtWidgets.QMessageBox.information(
            self,
            "Mailing",
            f"Fonctionnalité de mailing à implémenter.\n\n"
            f"{len(emails)} email(s) sélectionné(s) :\n" + "\n".join(emails[:10]) +
            ("\n..." if len(emails) > 10 else "")
        )

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