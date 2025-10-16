# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/cotisations_tab.py
Rôle : Onglet gestion des cotisations (CotisationsTab) du Club Manager.
Hérite de QWidget et de Ui_CotisationsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CotisationsTab généré par pyuic5 à partir de resources/ui/cotisations_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.cotisations_tab_ui import Ui_CotisationsTab

class CotisationsTab(QtWidgets.QWidget, Ui_CotisationsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddCotisation.clicked.connect(self.add_cotisation)
        self.buttonEditCotisation.clicked.connect(self.edit_cotisation)
        self.buttonDeleteCotisation.clicked.connect(self.delete_cotisation)
        self.buttonExportCotisations.clicked.connect(self.export_cotisations)
        self.tableCotisations.doubleClicked.connect(self.edit_cotisation)
        self.buttonRelance.clicked.connect(self.relance_cotisation)
        # Charger les cotisations au démarrage
        try:
            self.refresh_cotisations()
        except:
            pass  # La base n'est peut-être pas encore initialisée

    def add_cotisation(self):
        from club_manager.ui.cotisation_form_dialog import CotisationFormDialog
        from club_manager.core.cotisations import add_cotisation as add_cotisation_db
        dlg = CotisationFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            try:
                # Récupérer les valeurs
                member_id = int(dlg.editMember.text())  # TODO: À améliorer avec un combo box
                amount = float(dlg.editAmount.text() or '0')
                paid = float(dlg.editPaid.text() or '0')
                payment_date = dlg.datePaiement.date().toString("yyyy-MM-dd")
                method = dlg.comboMethod.currentText()
                status = dlg.comboStatus.currentText()
                
                # Récupérer le numéro de chèque si applicable
                cheque_number = None
                if method == "Chèque":
                    cheque_number = dlg.editChequeNumber.text()
                
                # Ajouter à la base (session_id mis à None)
                add_cotisation_db(member_id, None, amount, paid, payment_date, method, status, cheque_number)
                
                # Recharger la table
                self.refresh_cotisations()
                QtWidgets.QMessageBox.information(self, "Succès", "Cotisation ajoutée avec succès.")
            except ValueError as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Valeur invalide : {str(e)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de la cotisation : {str(e)}")

    def edit_cotisation(self):
        # Logique de modification de la cotisation sélectionnée
        selected_rows = self.tableCotisations.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner une cotisation à modifier.")
            return
        
        row = selected_rows[0].row()
        cotisation_id = self.tableCotisations.item(row, 0).data(QtWidgets.QTableWidgetItem.UserType)
        
        from club_manager.ui.cotisation_form_dialog import CotisationFormDialog
        from club_manager.core.cotisations import update_cotisation
        
        # Pour l'instant, on ne peut pas pré-remplir le dialog, donc on informe l'utilisateur
        QtWidgets.QMessageBox.information(
            self,
            "Modification",
            "La modification de cotisation nécessite une refonte du formulaire.\n"
            "Veuillez supprimer et recréer la cotisation."
        )

    def delete_cotisation(self):
        # Logique de suppression de la/des cotisations sélectionnées
        selected_rows = self.tableCotisations.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins une cotisation à supprimer.")
            return
        
        # Demander confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer {len(selected_rows)} cotisation(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            from club_manager.core.cotisations import delete_cotisation as delete_cotisation_db
            try:
                for row in selected_rows:
                    cotisation_id = self.tableCotisations.item(row.row(), 0).data(QtWidgets.QTableWidgetItem.UserType)
                    delete_cotisation_db(cotisation_id)
                
                # Recharger la table
                self.refresh_cotisations()
                QtWidgets.QMessageBox.information(self, "Succès", f"{len(selected_rows)} cotisation(s) supprimée(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_cotisations(self):
        # Exporter les cotisations
        from PyQt5.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les cotisations",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                from club_manager.core.cotisations import get_all_cotisations
                from club_manager.core.members import get_member_by_id
                
                cotisations = get_all_cotisations()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Membre', 'Montant', 'Payé', 'Date', 'Méthode', 'Statut']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for cotisation in cotisations:
                        try:
                            member = get_member_by_id(cotisation['member_id'])
                            member_name = f"{member['last_name']} {member['first_name']}" if member else "Inconnu"
                        except:
                            member_name = "Inconnu"
                        
                        method_text = cotisation['method'] or ''
                        if method_text == "Chèque" and cotisation.get('cheque_number'):
                            method_text += f" (N°{cotisation['cheque_number']})"
                        
                        writer.writerow({
                            'Membre': member_name,
                            'Montant': cotisation['amount'] or '0',
                            'Payé': cotisation['paid'] or '0',
                            'Date': cotisation['payment_date'] or '',
                            'Méthode': method_text,
                            'Statut': cotisation['status'] or ''
                        })
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Export réussi vers {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def relance_cotisation(self):
        # Relancer les membres en retard de paiement
        try:
            from club_manager.core.cotisations import get_late_members
            
            late_members = get_late_members()
            
            if not late_members:
                QtWidgets.QMessageBox.information(self, "Relance", "Aucun membre en retard de paiement.")
                return
            
            # Afficher la liste des membres en retard
            member_list = "\n".join([f"- {m['last_name']} {m['first_name']}" for m in late_members[:10]])
            if len(late_members) > 10:
                member_list += f"\n... et {len(late_members) - 10} autres"
            
            QtWidgets.QMessageBox.information(
                self,
                "Relance",
                f"{len(late_members)} membre(s) en retard de paiement :\n\n{member_list}\n\n"
                "La fonctionnalité d'envoi automatique de relance reste à implémenter."
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la relance : {str(e)}")

    def refresh_cotisations(self):
        # Recharge la table depuis la base
        from club_manager.core.cotisations import get_all_cotisations
        from club_manager.core.members import get_member_by_id
        
        cotisations = get_all_cotisations()
        self.tableCotisations.setRowCount(0)
        
        for row_idx, cotisation in enumerate(cotisations):
            self.tableCotisations.insertRow(row_idx)
            
            # Membre
            try:
                member = get_member_by_id(cotisation['member_id'])
                member_name = f"{member['last_name']} {member['first_name']}" if member else "Inconnu"
            except:
                member_name = "Inconnu"
            self.tableCotisations.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(member_name))
            
            # Montant
            self.tableCotisations.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(cotisation['amount'] or '0')))
            
            # Payé
            self.tableCotisations.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(cotisation['paid'] or '0')))
            
            # Date
            self.tableCotisations.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(cotisation['payment_date'] or '')))
            
            # Méthode
            method_text = cotisation['method'] or ''
            if method_text == "Chèque" and cotisation.get('cheque_number'):
                method_text += f" (N°{cotisation['cheque_number']})"
            self.tableCotisations.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(method_text))
            
            # Statut
            self.tableCotisations.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(str(cotisation['status'] or '')))
            
            # Stocker l'ID
            self.tableCotisations.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, cotisation['id'])