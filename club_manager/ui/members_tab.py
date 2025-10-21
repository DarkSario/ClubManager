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
import json

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
                    payment_type=payment_type,
                    ancv_amount=float(dlg.editANCVAmount.text() or '0'),
                    cash_amount=float(dlg.editCashAmount.text() or '0'),
                    check1_amount=float(dlg.editCheck1Amount.text() or '0'),
                    check2_amount=float(dlg.editCheck2Amount.text() or '0'),
                    check3_amount=float(dlg.editCheck3Amount.text() or '0'),
                    total_paid=float(dlg.editTotalPaid.text() or '0'),
                    mjc_club_id=mjc_club_id,
                    cotisation_status=dlg.comboCotisationStatus.currentText(),
                    birth_date=dlg.get_birth_date(),
                    other_mjc_clubs=dlg.get_other_mjc_clubs()
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
            dlg.editLastName.setText(member['last_name'] or '')
            dlg.editFirstName.setText(member['first_name'] or '')
            dlg.editAddress.setText(member['address'] or '')
            dlg.editPostalCode.setText(member['postal_code'] or '')
            dlg.editCity.setText(member['city'] or '')
            dlg.editPhone.setText(member['phone'] or '')
            dlg.editMail.setText(member['mail'] or '')
            dlg.checkRGPD.setChecked(bool(member['rgpd'] if member['rgpd'] is not None else 0))
            dlg.checkImageRights.setChecked(bool(member['image_rights'] if member['image_rights'] is not None else 0))
            
            # Restaurer la date de naissance
            from PyQt5.QtCore import QDate
            if member['birth_date']:
                date = QDate.fromString(member['birth_date'], "yyyy-MM-dd")
                if date.isValid():
                    dlg.editBirthDate.setDate(date)
            
            # Restaurer le type de paiement
            payment_type = member['payment_type'] if member['payment_type'] else 'club_mjc'
            if payment_type == 'club_only':
                dlg.comboPaymentType.setCurrentIndex(1)
                # Restaurer le club MJC sélectionné
                mjc_club_id = member['mjc_club_id']
                if mjc_club_id:
                    for i in range(dlg.comboMJCClub.count()):
                        if dlg.comboMJCClub.itemData(i) == mjc_club_id:
                            dlg.comboMJCClub.setCurrentIndex(i)
                            break
            else:
                dlg.comboPaymentType.setCurrentIndex(0)
            
            # Restaurer les montants de paiement
            dlg.editCashAmount.setText(str(member['cash_amount'] if member['cash_amount'] is not None else 0))
            dlg.editCheck1Amount.setText(str(member['check1_amount'] if member['check1_amount'] is not None else 0))
            dlg.editCheck2Amount.setText(str(member['check2_amount'] if member['check2_amount'] is not None else 0))
            dlg.editCheck3Amount.setText(str(member['check3_amount'] if member['check3_amount'] is not None else 0))
            dlg.editTotalPaid.setText(str(member['total_paid'] if member['total_paid'] is not None else 0))
            dlg.editANCVAmount.setText(str(member['ancv_amount'] if member['ancv_amount'] is not None else 0))
            
            # Restaurer le statut de cotisation
            status = member['cotisation_status'] if member['cotisation_status'] else 'Non payée'
            index = dlg.comboCotisationStatus.findText(status)
            if index >= 0:
                dlg.comboCotisationStatus.setCurrentIndex(index)
            
            # Restaurer les autres clubs MJC
            if member['other_mjc_clubs']:
                dlg.set_other_mjc_clubs(member['other_mjc_clubs'])
            
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
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
                    payment_type=payment_type,
                    ancv_amount=float(dlg.editANCVAmount.text() or '0'),
                    cash_amount=float(dlg.editCashAmount.text() or '0'),
                    check1_amount=float(dlg.editCheck1Amount.text() or '0'),
                    check2_amount=float(dlg.editCheck2Amount.text() or '0'),
                    check3_amount=float(dlg.editCheck3Amount.text() or '0'),
                    total_paid=float(dlg.editTotalPaid.text() or '0'),
                    mjc_club_id=mjc_club_id,
                    cotisation_status=dlg.comboCotisationStatus.currentText(),
                    birth_date=dlg.get_birth_date(),
                    other_mjc_clubs=dlg.get_other_mjc_clubs()
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
        from club_manager.ui.csv_export_dialog import CSVExportDialog
        from club_manager.core.exports import export_to_csv
        
        try:
            members = get_all_members()
            if not members:
                QtWidgets.QMessageBox.information(self, "Export", "Aucun membre à exporter.")
                return
            
            # Demander les options d'export CSV
            csv_dialog = CSVExportDialog(self)
            if csv_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            
            options = csv_dialog.get_options()
            
            # Demander le chemin de sauvegarde
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Exporter les membres",
                os.path.expanduser("~/membres_export.csv"),
                "Fichiers CSV (*.csv)"
            )
            
            if not file_path:
                return
            
            # Utiliser la fonction d'export centralisée avec les options choisies
            num_rows = export_to_csv(
                members,
                file_path,
                delimiter=options['delimiter'],
                add_bom=options['add_bom'],
                translate_headers=True
            )
            
            separator_name = {';': 'point-virgule', ',': 'virgule', '\t': 'tabulation'}
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{num_rows} membre(s) exporté(s) vers :\n{file_path}\n\n"
                f"Séparateur : {separator_name.get(options['delimiter'], options['delimiter'])}\n"
                f"BOM UTF-8 : {'Oui' if options['add_bom'] else 'Non'}"
            )
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            QtWidgets.QMessageBox.critical(
                self, 
                "Erreur d'export", 
                f"Erreur lors de l'export : {str(e)}\n\nDétails:\n{error_details}"
            )

    def filter_members(self):
        """Filtre les membres selon les critères saisis."""
        from club_manager.ui.member_filter_dialog import MemberFilterDialog
        from club_manager.core.members import get_filtered_members
        from club_manager.core.mjc_clubs import get_mjc_club_by_id
        
        # Ouvrir le dialogue de filtrage
        dlg = MemberFilterDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            filters = dlg.get_filters()
            
            if not filters:
                QtWidgets.QMessageBox.information(
                    self,
                    "Aucun filtre",
                    "Aucun critère de filtrage n'a été saisi."
                )
                return
            
            try:
                # Stocker les filtres actuels
                self._current_filter = filters
                
                # Récupérer les membres filtrés
                members = get_filtered_members(filters)
                
                # Mettre à jour le résumé des paiements avec les membres filtrés
                self.update_payment_summary(members)
                
                # Mettre à jour le tableau
                self.tableMembers.setRowCount(0)
                
                if not members:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Aucun résultat",
                        "Aucun membre ne correspond aux critères de recherche."
                    )
                    return
                
                # Afficher les membres filtrés
                for row_idx, member in enumerate(members):
                    self.tableMembers.insertRow(row_idx)
                    
                    # Nom, Prénom, Adresse, CP, Ville, Tél, Mail
                    self.tableMembers.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(member['last_name'] or '')))
                    self.tableMembers.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(member['first_name'] or '')))
                    self.tableMembers.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(member['address'] or '')))
                    self.tableMembers.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(member['postal_code'] or '')))
                    self.tableMembers.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(member['city'] or '')))
                    self.tableMembers.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(str(member['phone'] or '')))
                    self.tableMembers.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(member['mail'] or '')))
                    
                    # Date de naissance (formatée dd/MM/yyyy)
                    birth_date_str = ''
                    if member['birth_date']:
                        from PyQt5.QtCore import QDate
                        date = QDate.fromString(member['birth_date'], "yyyy-MM-dd")
                        if date.isValid():
                            birth_date_str = date.toString("dd/MM/yyyy")
                    self.tableMembers.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(birth_date_str))
                    
                    # RGPD, Droit image
                    self.tableMembers.setItem(row_idx, 8, QtWidgets.QTableWidgetItem('Oui' if member['rgpd'] else 'Non'))
                    self.tableMembers.setItem(row_idx, 9, QtWidgets.QTableWidgetItem('Oui' if member['image_rights'] else 'Non'))
                    
                    # Montants de paiement
                    self.tableMembers.setItem(row_idx, 10, QtWidgets.QTableWidgetItem(str(member['cash_amount'] if member['cash_amount'] is not None else '0')))
                    self.tableMembers.setItem(row_idx, 11, QtWidgets.QTableWidgetItem(str(member['check1_amount'] if member['check1_amount'] is not None else '0')))
                    self.tableMembers.setItem(row_idx, 12, QtWidgets.QTableWidgetItem(str(member['check2_amount'] if member['check2_amount'] is not None else '0')))
                    self.tableMembers.setItem(row_idx, 13, QtWidgets.QTableWidgetItem(str(member['check3_amount'] if member['check3_amount'] is not None else '0')))
                    self.tableMembers.setItem(row_idx, 14, QtWidgets.QTableWidgetItem(str(member['ancv_amount'] if member['ancv_amount'] is not None else '0')))
                    self.tableMembers.setItem(row_idx, 15, QtWidgets.QTableWidgetItem(str(member['total_paid'] if member['total_paid'] is not None else '0')))
                    
                    # Club MJC cotisation
                    mjc_club_name = ''
                    if member['mjc_club_id']:
                        try:
                            mjc_club = get_mjc_club_by_id(member['mjc_club_id'])
                            if mjc_club:
                                mjc_club_name = mjc_club['name']
                        except:
                            pass
                    self.tableMembers.setItem(row_idx, 16, QtWidgets.QTableWidgetItem(mjc_club_name))
                    
                    # Autres clubs MJC
                    other_clubs_str = ''
                    if member['other_mjc_clubs']:
                        try:
                            club_ids = json.loads(member['other_mjc_clubs'])
                            club_names = []
                            for club_id in club_ids:
                                club = get_mjc_club_by_id(club_id)
                                if club:
                                    club_names.append(club['name'])
                            other_clubs_str = ', '.join(club_names)
                        except (json.JSONDecodeError, TypeError, ValueError):
                            pass
                    self.tableMembers.setItem(row_idx, 17, QtWidgets.QTableWidgetItem(other_clubs_str))
                    
                    # Statut cotisation
                    self.tableMembers.setItem(row_idx, 18, QtWidgets.QTableWidgetItem(str(member['cotisation_status'] or 'Non payée')))
                    
                    # Stocker l'ID du membre dans la première colonne avec Qt.UserRole
                    self.tableMembers.item(row_idx, 0).setData(Qt.UserRole, member['id'])
                
                # Afficher un message de confirmation
                QtWidgets.QMessageBox.information(
                    self,
                    "Filtrage réussi",
                    f"{len(members)} membre(s) correspond(ent) aux critères de recherche."
                )
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Erreur de filtrage",
                    f"Erreur lors du filtrage : {str(e)}"
                )

    def reset_filter(self):
        """Réinitialise tous les filtres et recharge tous les membres."""
        self._current_filter = {}
        self.refresh_members()

    def do_mailing(self):
        """Ouvre l'onglet Mailing."""
        # Récupérer la fenêtre principale
        main_window = self.window()
        if hasattr(main_window, 'tabs'):
            # Trouver l'index de l'onglet Mailing
            for i in range(main_window.tabs.count()):
                if main_window.tabs.tabText(i) == "Mailing":
                    main_window.tabs.setCurrentIndex(i)
                    QtWidgets.QMessageBox.information(
                        self,
                        "Mailing",
                        "L'onglet Mailing a été ouvert.\n\n"
                        "Utilisez le bouton 'Sélection destinataires' pour choisir les membres, "
                        "puis configurez vos paramètres SMTP si ce n'est pas déjà fait."
                    )
                    return
        
        QtWidgets.QMessageBox.information(
            self,
            "Mailing",
            "Utilisez l'onglet Mailing pour envoyer des emails groupés.\n\n"
            "Pensez à configurer les paramètres SMTP avant l'envoi."
        )

    def update_payment_summary(self, members):
        """Met à jour les labels de résumé des paiements.
        
        Args:
            members: Liste des membres à partir desquels calculer les totaux
        """
        from club_manager.core.utils import calculate_payment_totals, format_currency
        
        totals = calculate_payment_totals(members)
        
        self.labelTotalAmount.setText(f"Total général : {format_currency(totals['total'])}")
        self.labelCashAmount.setText(f"Espèces : {format_currency(totals['cash'])}")
        self.labelChecksAmount.setText(f"Chèques : {format_currency(totals['checks'])}")
        self.labelAncvAmount.setText(f"ANCV : {format_currency(totals['ancv'])}")

    def refresh_members(self):
        """Recharge la table des membres depuis la base de données."""
        from club_manager.core.members import get_all_members
        from club_manager.core.mjc_clubs import get_mjc_club_by_id
        
        members = get_all_members()
        self.tableMembers.setRowCount(0)
        
        # Mettre à jour le résumé des paiements
        self.update_payment_summary(members)
        
        for row_idx, member in enumerate(members):
            self.tableMembers.insertRow(row_idx)
            
            # Nom, Prénom, Adresse, CP, Ville, Tél, Mail
            self.tableMembers.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(member['last_name'] or '')))
            self.tableMembers.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(member['first_name'] or '')))
            self.tableMembers.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(member['address'] or '')))
            self.tableMembers.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(member['postal_code'] or '')))
            self.tableMembers.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(member['city'] or '')))
            self.tableMembers.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(str(member['phone'] or '')))
            self.tableMembers.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(member['mail'] or '')))
            
            # Date de naissance (formatée dd/MM/yyyy)
            birth_date_str = ''
            if member['birth_date']:
                from PyQt5.QtCore import QDate
                date = QDate.fromString(member['birth_date'], "yyyy-MM-dd")
                if date.isValid():
                    birth_date_str = date.toString("dd/MM/yyyy")
            self.tableMembers.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(birth_date_str))
            
            # RGPD, Droit image
            self.tableMembers.setItem(row_idx, 8, QtWidgets.QTableWidgetItem('Oui' if member['rgpd'] else 'Non'))
            self.tableMembers.setItem(row_idx, 9, QtWidgets.QTableWidgetItem('Oui' if member['image_rights'] else 'Non'))
            
            # Montants de paiement
            self.tableMembers.setItem(row_idx, 10, QtWidgets.QTableWidgetItem(str(member['cash_amount'] if member['cash_amount'] is not None else '0')))
            self.tableMembers.setItem(row_idx, 11, QtWidgets.QTableWidgetItem(str(member['check1_amount'] if member['check1_amount'] is not None else '0')))
            self.tableMembers.setItem(row_idx, 12, QtWidgets.QTableWidgetItem(str(member['check2_amount'] if member['check2_amount'] is not None else '0')))
            self.tableMembers.setItem(row_idx, 13, QtWidgets.QTableWidgetItem(str(member['check3_amount'] if member['check3_amount'] is not None else '0')))
            self.tableMembers.setItem(row_idx, 14, QtWidgets.QTableWidgetItem(str(member['ancv_amount'] if member['ancv_amount'] is not None else '0')))
            self.tableMembers.setItem(row_idx, 15, QtWidgets.QTableWidgetItem(str(member['total_paid'] if member['total_paid'] is not None else '0')))
            
            # Club MJC cotisation
            mjc_club_name = ''
            if member['mjc_club_id']:
                try:
                    mjc_club = get_mjc_club_by_id(member['mjc_club_id'])
                    if mjc_club:
                        mjc_club_name = mjc_club['name']
                except:
                    pass
            self.tableMembers.setItem(row_idx, 16, QtWidgets.QTableWidgetItem(mjc_club_name))
            
            # Autres clubs MJC
            other_clubs_str = ''
            if member['other_mjc_clubs']:
                try:
                    club_ids = json.loads(member['other_mjc_clubs'])
                    club_names = []
                    for club_id in club_ids:
                        club = get_mjc_club_by_id(club_id)
                        if club:
                            club_names.append(club['name'])
                    other_clubs_str = ', '.join(club_names)
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass
            self.tableMembers.setItem(row_idx, 17, QtWidgets.QTableWidgetItem(other_clubs_str))
            
            # Statut cotisation
            self.tableMembers.setItem(row_idx, 18, QtWidgets.QTableWidgetItem(str(member['cotisation_status'] or 'Non payée')))
            
            # Stocker l'ID du membre dans la première colonne avec Qt.UserRole
            self.tableMembers.item(row_idx, 0).setData(Qt.UserRole, member['id'])