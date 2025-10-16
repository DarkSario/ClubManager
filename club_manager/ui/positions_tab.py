# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/positions_tab.py
Rôle : Onglet gestion des postes (PositionsTab) du Club Manager.
Hérite de QWidget et de Ui_PositionsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_PositionsTab généré par pyuic5 à partir de resources/ui/positions_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.positions_tab_ui import Ui_PositionsTab

class PositionsTab(QtWidgets.QWidget, Ui_PositionsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddPosition.clicked.connect(self.add_position)
        self.buttonEditPosition.clicked.connect(self.edit_position)
        self.buttonDeletePosition.clicked.connect(self.delete_position)
        self.buttonExportPositions.clicked.connect(self.export_positions)
        self.tablePositions.doubleClicked.connect(self.edit_position)
        self.buttonAffect.clicked.connect(self.affect_position)
        self.buttonUnaffect.clicked.connect(self.unaffect_position)
        # Charger les postes au démarrage
        try:
            self.refresh_positions()
        except:
            pass  # La base n'est peut-être pas encore initialisée

    def add_position(self):
        from club_manager.ui.position_form_dialog import PositionFormDialog
        dlg = PositionFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_positions()

    def edit_position(self):
        # Logique de modification du poste sélectionné
        selected_rows = self.tablePositions.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner un poste à modifier.")
            return
        
        QtWidgets.QMessageBox.information(
            self,
            "Modification",
            "La modification de poste nécessite une refonte du formulaire.\n"
            "Veuillez supprimer et recréer le poste."
        )

    def delete_position(self):
        # Logique de suppression du/des postes sélectionnés
        selected_rows = self.tablePositions.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un poste à supprimer.")
            return
        
        # Demander confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer {len(selected_rows)} poste(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            from club_manager.core.positions import delete_position as delete_position_db
            try:
                for row in selected_rows:
                    position_id = self.tablePositions.item(row.row(), 0).data(QtWidgets.QTableWidgetItem.UserType)
                    delete_position_db(position_id)
                
                # Recharger la table
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", f"{len(selected_rows)} poste(s) supprimé(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_positions(self):
        # Exporter les postes
        from PyQt5.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les postes",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                from club_manager.core.positions import get_all_positions
                from club_manager.core.members import get_member_by_id
                
                positions = get_all_positions()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nom', 'Type', 'Description', 'Affecté à']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for position in positions:
                        assigned_to = ""
                        if position.get('assigned_to'):
                            try:
                                member = get_member_by_id(position['assigned_to'])
                                assigned_to = f"{member['last_name']} {member['first_name']}" if member else ""
                            except:
                                pass
                        
                        writer.writerow({
                            'Nom': position['name'] or '',
                            'Type': position['type'] or '',
                            'Description': position['description'] or '',
                            'Affecté à': assigned_to
                        })
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Export réussi vers {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def affect_position(self):
        # Affecter un poste à un membre
        selected_rows = self.tablePositions.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner un poste à affecter.")
            return
        
        # Demander l'ID du membre
        member_id, ok = QtWidgets.QInputDialog.getInt(
            self,
            "Affecter un poste",
            "Entrez l'ID du membre à affecter au poste:",
            min=1
        )
        
        if ok:
            from club_manager.core.positions import update_position, get_all_positions
            from club_manager.core.members import get_member_by_id
            
            try:
                # Vérifier que le membre existe
                member = get_member_by_id(member_id)
                if not member:
                    QtWidgets.QMessageBox.warning(self, "Erreur", "Membre introuvable.")
                    return
                
                # Affecter le poste
                row = selected_rows[0].row()
                position_id = self.tablePositions.item(row, 0).data(QtWidgets.QTableWidgetItem.UserType)
                
                # Récupérer les données actuelles du poste
                positions = get_all_positions()
                position = next((p for p in positions if p['id'] == position_id), None)
                
                if position:
                    update_position(
                        position_id,
                        position['name'],
                        position['type'],
                        position['description'],
                        member_id
                    )
                    self.refresh_positions()
                    QtWidgets.QMessageBox.information(
                        self,
                        "Succès",
                        f"Poste affecté à {member['last_name']} {member['first_name']}."
                    )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affectation : {str(e)}")

    def unaffect_position(self):
        # Désaffecter un poste d'un membre
        selected_rows = self.tablePositions.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner un poste à désaffecter.")
            return
        
        from club_manager.core.positions import update_position, get_all_positions
        
        try:
            row = selected_rows[0].row()
            position_id = self.tablePositions.item(row, 0).data(QtWidgets.QTableWidgetItem.UserType)
            
            # Récupérer les données actuelles du poste
            positions = get_all_positions()
            position = next((p for p in positions if p['id'] == position_id), None)
            
            if position:
                update_position(
                    position_id,
                    position['name'],
                    position['type'],
                    position['description'],
                    None
                )
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", "Poste désaffecté avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la désaffectation : {str(e)}")

    def refresh_positions(self):
        # Recharge la table depuis la base
        from club_manager.core.positions import get_all_positions
        from club_manager.core.members import get_member_by_id
        
        positions = get_all_positions()
        self.tablePositions.setRowCount(0)
        
        for row_idx, position in enumerate(positions):
            self.tablePositions.insertRow(row_idx)
            
            # Nom
            self.tablePositions.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(position['name'] or '')))
            
            # Type
            self.tablePositions.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(position['type'] or '')))
            
            # Description
            self.tablePositions.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(position['description'] or '')))
            
            # Affecté à
            assigned_to = ""
            if position.get('assigned_to'):
                try:
                    member = get_member_by_id(position['assigned_to'])
                    assigned_to = f"{member['last_name']} {member['first_name']}" if member else ""
                except:
                    pass
            self.tablePositions.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(assigned_to))
            
            # Stocker l'ID
            self.tablePositions.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, position['id'])