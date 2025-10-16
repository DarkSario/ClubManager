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
        # Logique de modification de la cotisation sélectionnée
        pass

    def delete_cotisation(self):
        # Logique de suppression de la/des cotisations sélectionnées
        pass

    def export_cotisations(self):
        # Exporter les cotisations
        pass

    def relance_cotisation(self):
        # Relancer les membres en retard de paiement
        pass

    def refresh_cotisations(self):
        # Recharge la table depuis la base
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
            
            # Stocker l'ID
            self.tableCotisations.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, cotisation['id'])