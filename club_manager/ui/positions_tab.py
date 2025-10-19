# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/positions_tab.py
Rôle : Onglet gestion des postes (PositionsTab) du Club Manager.
Hérite de QWidget et de Ui_PositionsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_PositionsTab généré par pyuic5 à partir de resources/ui/positions_tab.ui
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from club_manager.ui.positions_tab_ui import Ui_PositionsTab
import csv
import os

class PositionsTab(QtWidgets.QWidget, Ui_PositionsTab):
    """Onglet de gestion des postes avec CRUD complet et affectations."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connexions
        self.buttonAddPosition.clicked.connect(self.add_position)
        self.buttonEditPosition.clicked.connect(self.edit_position)
        self.buttonDeletePosition.clicked.connect(self.delete_position)
        self.buttonExportPositions.clicked.connect(self.export_positions)
        self.tablePositions.doubleClicked.connect(self.edit_position)
        self.buttonAffect.clicked.connect(self.affect_position)
        self.buttonUnaffect.clicked.connect(self.unaffect_position)
        
        # Charger au démarrage
        try:
            self.refresh_positions()
        except:
            pass

    def add_position(self):
        """Ajoute un nouveau poste."""
        from club_manager.ui.position_form_dialog import PositionFormDialog
        from club_manager.core.positions import add_position as add_position_db
        
        dlg = PositionFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Validation
            if not dlg.editName.text():
                QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le nom du poste est obligatoire.")
                return
            
            try:
                add_position_db(
                    name=dlg.editName.text(),
                    type=dlg.comboType.currentText() if hasattr(dlg, 'comboType') else '',
                    description=dlg.editDescription.toPlainText() if hasattr(dlg, 'editDescription') else '',
                    assigned_to=None
                )
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", "Poste ajouté avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout : {str(e)}")

    def edit_position(self):
        """Édite le poste sélectionné."""
        from club_manager.ui.position_form_dialog import PositionFormDialog
        from club_manager.core.positions import get_all_positions, update_position
        
        selected_items = self.tablePositions.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un poste à modifier.")
            return
        
        row = selected_items[0].row()
        position_id = self.tablePositions.item(row, 0).data(Qt.UserRole)
        
        if not position_id:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de récupérer l'ID du poste.")
            return
        
        try:
            positions = get_all_positions()
            position = next((p for p in positions if p['id'] == position_id), None)
            
            if not position:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Poste introuvable.")
                return
            
            # Pré-remplir le formulaire
            dlg = PositionFormDialog(self)
            dlg.setWindowTitle("Modifier un poste")
            dlg.editName.setText(position.get('name', ''))
            
            if hasattr(dlg, 'comboType'):
                type_index = dlg.comboType.findText(position.get('type', ''))
                if type_index >= 0:
                    dlg.comboType.setCurrentIndex(type_index)
            
            if hasattr(dlg, 'editDescription'):
                dlg.editDescription.setPlainText(position.get('description', ''))
            
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                if not dlg.editName.text():
                    QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le nom du poste est obligatoire.")
                    return
                
                update_position(
                    position_id,
                    name=dlg.editName.text(),
                    type=dlg.comboType.currentText() if hasattr(dlg, 'comboType') else '',
                    description=dlg.editDescription.toPlainText() if hasattr(dlg, 'editDescription') else '',
                    assigned_to=position.get('assigned_to')  # Conserver l'affectation
                )
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", "Poste modifié avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")

    def delete_position(self):
        """Supprime le(s) poste(s) sélectionné(s) après confirmation."""
        from club_manager.core.positions import delete_position as delete_position_db
        
        selected_items = self.tablePositions.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un ou plusieurs postes à supprimer."
            )
            return
        
        selected_rows = set(item.row() for item in selected_items)
        position_count = len(selected_rows)
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer {position_count} poste(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    position_id = self.tablePositions.item(row, 0).data(Qt.UserRole)
                    if position_id:
                        delete_position_db(position_id)
                
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", f"{position_count} poste(s) supprimé(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_positions(self):
        """Exporte la liste des postes en CSV."""
        from club_manager.core.positions import get_all_positions
        from club_manager.ui.csv_export_dialog import CSVExportDialog
        from club_manager.core.exports import export_to_csv
        
        try:
            positions = get_all_positions()
            if not positions:
                QtWidgets.QMessageBox.information(self, "Export", "Aucun poste à exporter.")
                return
            
            # Demander les options d'export CSV
            csv_dialog = CSVExportDialog(self)
            if csv_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            
            options = csv_dialog.get_options()
            
            # Demander le chemin de sauvegarde
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Exporter les postes",
                os.path.expanduser("~/postes_export.csv"),
                "Fichiers CSV (*.csv)"
            )
            
            if not file_path:
                return
            
            # Utiliser la fonction d'export centralisée avec les options choisies
            num_rows = export_to_csv(
                positions,
                file_path,
                delimiter=options['delimiter'],
                add_bom=options['add_bom'],
                translate_headers=True
            )
            
            separator_name = {';': 'point-virgule', ',': 'virgule', '\t': 'tabulation'}
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{num_rows} poste(s) exporté(s) vers :\n{file_path}\n\n"
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

    def affect_position(self):
        """Affecte le poste sélectionné à un membre."""
        from club_manager.core.positions import get_all_positions, update_position
        from club_manager.core.members import get_all_members
        
        selected_items = self.tablePositions.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un poste à affecter.")
            return
        
        row = selected_items[0].row()
        position_id = self.tablePositions.item(row, 0).data(Qt.UserRole)
        
        if not position_id:
            return
        
        try:
            positions = get_all_positions()
            position = next((p for p in positions if p['id'] == position_id), None)
            
            if not position:
                return
            
            # Récupérer la liste des membres
            members = get_all_members()
            if not members:
                QtWidgets.QMessageBox.warning(self, "Aucun membre", "Aucun membre disponible pour l'affectation.")
                return
            
            # Créer un dialogue de sélection
            member_names = [f"{m['last_name']} {m['first_name']}" for m in members]
            member_name, ok = QtWidgets.QInputDialog.getItem(
                self,
                "Affecter un poste",
                "Sélectionnez le membre à affecter :",
                member_names,
                0,
                False
            )
            
            if ok and member_name:
                # Trouver l'ID du membre
                member_index = member_names.index(member_name)
                member_id = members[member_index]['id']
                
                update_position(
                    position_id,
                    name=position['name'],
                    type=position.get('type', ''),
                    description=position.get('description', ''),
                    assigned_to=member_id
                )
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", "Poste affecté avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affectation : {str(e)}")

    def unaffect_position(self):
        """Désaffecte le poste sélectionné."""
        from club_manager.core.positions import get_all_positions, update_position
        
        selected_items = self.tablePositions.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un poste à désaffecter.")
            return
        
        row = selected_items[0].row()
        position_id = self.tablePositions.item(row, 0).data(Qt.UserRole)
        
        if not position_id:
            return
        
        try:
            positions = get_all_positions()
            position = next((p for p in positions if p['id'] == position_id), None)
            
            if not position:
                return
            
            if not position.get('assigned_to'):
                QtWidgets.QMessageBox.information(self, "Info", "Ce poste n'est pas affecté.")
                return
            
            reply = QtWidgets.QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous vraiment désaffecter ce poste ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                update_position(
                    position_id,
                    name=position['name'],
                    type=position.get('type', ''),
                    description=position.get('description', ''),
                    assigned_to=None
                )
                self.refresh_positions()
                QtWidgets.QMessageBox.information(self, "Succès", "Poste désaffecté avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la désaffectation : {str(e)}")

    def refresh_positions(self):
        """Recharge la table des postes depuis la base de données."""
        from club_manager.core.positions import get_all_positions
        from club_manager.core.members import get_member_by_id
        
        positions = get_all_positions()
        self.tablePositions.setRowCount(0)
        
        for row_idx, position in enumerate(positions):
            self.tablePositions.insertRow(row_idx)
            self.tablePositions.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(position['name'] or '')))
            self.tablePositions.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(position.get('type', '') or '')))
            self.tablePositions.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(position.get('description', '') or '')))
            
            # Afficher le nom du membre affecté
            assigned_name = "Non affecté"
            if position.get('assigned_to'):
                try:
                    member = get_member_by_id(position['assigned_to'])
                    if member:
                        assigned_name = f"{member['last_name']} {member['first_name']}"
                except:
                    pass
            
            self.tablePositions.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(assigned_name))
            
            # Stocker l'ID avec Qt.UserRole
            self.tablePositions.item(row_idx, 0).setData(Qt.UserRole, position['id'])