# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/cotisations_tab.py
Rôle : Onglet gestion des cotisations (CotisationsTab) du Club Manager.
Hérite de QWidget et de Ui_CotisationsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CotisationsTab généré par pyuic5 à partir de resources/ui/cotisations_tab.ui
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from club_manager.ui.cotisations_tab_ui import Ui_CotisationsTab
import csv
import os

class CotisationsTab(QtWidgets.QWidget, Ui_CotisationsTab):
    """Onglet de gestion des cotisations avec CRUD complet et relances."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connexions des boutons
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
                session_id = int(dlg.editSession.text())  # TODO: À améliorer avec un combo box
                amount = float(dlg.editAmount.text() or '0')
                paid = float(dlg.editPaid.text() or '0')
                payment_date = dlg.datePaiement.date().toString("yyyy-MM-dd")
                method = dlg.comboMethod.currentText()
                status = dlg.comboStatus.currentText()
                
                # Récupérer le numéro de chèque si applicable
                cheque_number = None
                if method == "Chèque":
                    cheque_number = dlg.editChequeNumber.text()
                
                # Ajouter à la base
                add_cotisation_db(member_id, session_id, amount, paid, payment_date, method, status, cheque_number)
                
                # Recharger la table
                self.refresh_cotisations()
                QtWidgets.QMessageBox.information(self, "Succès", "Cotisation ajoutée avec succès.")
            except ValueError as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Valeur invalide : {str(e)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de la cotisation : {str(e)}")

    def edit_cotisation(self):
        """Édite la cotisation sélectionnée."""
        from club_manager.ui.cotisation_form_dialog import CotisationFormDialog
        from club_manager.core.cotisations import get_all_cotisations, update_cotisation
        
        selected_items = self.tableCotisations.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner une cotisation à modifier."
            )
            return
        
        row = selected_items[0].row()
        cotisation_id = self.tableCotisations.item(row, 0).data(Qt.UserRole)
        
        if not cotisation_id:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de récupérer l'ID de la cotisation.")
            return
        
        try:
            # Récupérer la cotisation
            cotisations = get_all_cotisations()
            cotisation = next((c for c in cotisations if c['id'] == cotisation_id), None)
            
            if not cotisation:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Cotisation introuvable.")
                return
            
            # Pré-remplir le formulaire
            dlg = CotisationFormDialog(self)
            dlg.setWindowTitle("Modifier une cotisation")
            dlg.editMember.setText(str(cotisation.get('member_id', '')))
            dlg.editSession.setText(str(cotisation.get('session_id', '')))
            dlg.editAmount.setText(str(cotisation.get('amount', 0)))
            dlg.editPaid.setText(str(cotisation.get('paid', 0)))
            
            # Date de paiement
            from PyQt5.QtCore import QDate
            payment_date = cotisation.get('payment_date', '')
            if payment_date:
                date_parts = payment_date.split('-')
                if len(date_parts) == 3:
                    dlg.datePaiement.setDate(QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2])))
            
            # Méthode et statut
            method = cotisation.get('method', '')
            status = cotisation.get('status', '')
            
            method_index = dlg.comboMethod.findText(method)
            if method_index >= 0:
                dlg.comboMethod.setCurrentIndex(method_index)
            
            status_index = dlg.comboStatus.findText(status)
            if status_index >= 0:
                dlg.comboStatus.setCurrentIndex(status_index)
            
            # Numéro de chèque si applicable
            if cotisation.get('cheque_number'):
                dlg.editChequeNumber.setText(cotisation.get('cheque_number', ''))
            
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                try:
                    member_id = int(dlg.editMember.text())
                    session_id = int(dlg.editSession.text())
                    amount = float(dlg.editAmount.text() or '0')
                    paid = float(dlg.editPaid.text() or '0')
                    payment_date = dlg.datePaiement.date().toString("yyyy-MM-dd")
                    method = dlg.comboMethod.currentText()
                    status = dlg.comboStatus.currentText()
                    
                    cheque_number = None
                    if method == "Chèque":
                        cheque_number = dlg.editChequeNumber.text()
                        if not cheque_number:
                            QtWidgets.QMessageBox.warning(
                                self,
                                "Numéro de chèque requis",
                                "Le numéro de chèque est obligatoire pour un paiement par chèque."
                            )
                            return
                    
                    update_cotisation(
                        cotisation_id,
                        member_id,
                        session_id,
                        amount,
                        paid,
                        payment_date,
                        method,
                        status,
                        cheque_number
                    )
                    
                    self.refresh_cotisations()
                    QtWidgets.QMessageBox.information(self, "Succès", "Cotisation modifiée avec succès.")
                except ValueError as e:
                    QtWidgets.QMessageBox.critical(self, "Erreur", f"Valeur invalide : {str(e)}")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")

    def delete_cotisation(self):
        """Supprime la/les cotisation(s) sélectionnée(s) après confirmation."""
        from club_manager.core.cotisations import delete_cotisation as delete_cotisation_db
        
        selected_items = self.tableCotisations.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner une ou plusieurs cotisations à supprimer."
            )
            return
        
        selected_rows = set(item.row() for item in selected_items)
        cotisation_count = len(selected_rows)
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer {cotisation_count} cotisation(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    cotisation_id = self.tableCotisations.item(row, 0).data(Qt.UserRole)
                    if cotisation_id:
                        delete_cotisation_db(cotisation_id)
                
                self.refresh_cotisations()
                QtWidgets.QMessageBox.information(
                    self,
                    "Succès",
                    f"{cotisation_count} cotisation(s) supprimée(s) avec succès."
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_cotisations(self):
        """Exporte la liste des cotisations en CSV."""
        from club_manager.core.cotisations import get_all_cotisations
        from club_manager.ui.csv_export_dialog import CSVExportDialog
        from club_manager.core.exports import export_to_csv
        
        try:
            cotisations = get_all_cotisations()
            if not cotisations:
                QtWidgets.QMessageBox.information(self, "Export", "Aucune cotisation à exporter.")
                return
            
            # Demander les options d'export CSV
            csv_dialog = CSVExportDialog(self)
            if csv_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            
            options = csv_dialog.get_options()
            
            # Demander le chemin de sauvegarde
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Exporter les cotisations",
                os.path.expanduser("~/cotisations_export.csv"),
                "Fichiers CSV (*.csv)"
            )
            
            if not file_path:
                return
            
            # Utiliser la fonction d'export centralisée avec les options choisies
            num_rows = export_to_csv(
                cotisations,
                file_path,
                delimiter=options['delimiter'],
                add_bom=options['add_bom'],
                translate_headers=True
            )
            
            separator_name = {';': 'point-virgule', ',': 'virgule', '\t': 'tabulation'}
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{num_rows} cotisation(s) exportée(s) vers :\n{file_path}\n\n"
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

    def relance_cotisation(self):
        """Relance les membres en retard de paiement."""
        from club_manager.core.cotisations import get_late_members
        
        try:
            late_members = get_late_members()
            
            if not late_members:
                QtWidgets.QMessageBox.information(
                    self,
                    "Relances",
                    "Aucun membre en retard de paiement."
                )
                return
            
            # Construire la liste des membres
            names = [f"{m['last_name']} {m['first_name']}" for m in late_members]
            message = f"{len(late_members)} membre(s) en retard de paiement :\n\n"
            message += "\n".join(names[:10])
            
            if len(late_members) > 10:
                message += f"\n... et {len(late_members) - 10} autre(s)"
            
            message += "\n\nLa fonctionnalité d'envoi automatique de relances sera disponible via l'onglet Mailing."
            
            QtWidgets.QMessageBox.information(self, "Relances", message)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des relances : {str(e)}")

    def refresh_cotisations(self):
        """Recharge la table des cotisations depuis la base de données."""
        from club_manager.core.cotisations import get_all_cotisations
        from club_manager.core.members import get_member_by_id
        from club_manager.core.sessions import get_all_sessions
        
        cotisations = get_all_cotisations()
        self.tableCotisations.setRowCount(0)
        
        # Créer des maps pour les noms
        sessions_map = {}
        try:
            sessions = get_all_sessions()
            sessions_map = {s['id']: s['name'] for s in sessions}
        except:
            pass
        
        for row_idx, cotisation in enumerate(cotisations):
            self.tableCotisations.insertRow(row_idx)
            
            # Membre
            try:
                member = get_member_by_id(cotisation['member_id'])
                member_name = f"{member['last_name']} {member['first_name']}" if member else "Inconnu"
            except:
                member_name = "Inconnu"
            self.tableCotisations.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(member_name))
            
            # Session
            session_name = sessions_map.get(cotisation['session_id'], "N/A")
            self.tableCotisations.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(session_name))
            
            # Montant
            self.tableCotisations.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(cotisation['amount'] or '0')))
            
            # Payé
            self.tableCotisations.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(cotisation['paid'] or '0')))
            
            # Date
            self.tableCotisations.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(cotisation['payment_date'] or '')))
            
            # Méthode
            method_text = cotisation['method'] or ''
            if method_text == "Chèque" and cotisation.get('cheque_number'):
                method_text += f" (N°{cotisation['cheque_number']})"
            self.tableCotisations.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(method_text))
            
            # Statut
            self.tableCotisations.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(cotisation['status'] or '')))
            
            # Stocker l'ID avec Qt.UserRole
            self.tableCotisations.item(row_idx, 0).setData(Qt.UserRole, cotisation['id'])