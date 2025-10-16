# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/custom_fields_tab.py
Rôle : Onglet gestion des champs personnalisés (CustomFieldsTab) du Club Manager.
Hérite de QWidget et de Ui_CustomFieldsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CustomFieldsTab généré par pyuic5 à partir de resources/ui/custom_fields_tab.ui
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from club_manager.ui.custom_fields_tab_ui import Ui_CustomFieldsTab
import csv
import os

class CustomFieldsTab(QtWidgets.QWidget, Ui_CustomFieldsTab):
    """Onglet de gestion des champs personnalisés avec CRUD complet."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connexions
        self.buttonAddCustomField.clicked.connect(self.add_custom_field)
        self.buttonEditCustomField.clicked.connect(self.edit_custom_field)
        self.buttonDeleteCustomField.clicked.connect(self.delete_custom_field)
        self.buttonExportCustomFields.clicked.connect(self.export_custom_fields)
        self.tableCustomFields.doubleClicked.connect(self.edit_custom_field)
        
        # Charger au démarrage
        try:
            self.refresh_custom_fields()
        except:
            pass

    def add_custom_field(self):
        """Ajoute un nouveau champ personnalisé."""
        from club_manager.ui.custom_field_form_dialog import CustomFieldFormDialog
        from club_manager.core.custom_fields import add_custom_field as add_field_db
        
        dlg = CustomFieldFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Validation
            if not dlg.editName.text():
                QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le nom du champ est obligatoire.")
                return
            
            try:
                add_field_db(
                    name=dlg.editName.text(),
                    ftype=dlg.comboType.currentText() if hasattr(dlg, 'comboType') else 'text',
                    default_value=dlg.editDefaultValue.text() if hasattr(dlg, 'editDefaultValue') else '',
                    options=dlg.editOptions.text() if hasattr(dlg, 'editOptions') else '',
                    constraints=dlg.editConstraints.text() if hasattr(dlg, 'editConstraints') else ''
                )
                self.refresh_custom_fields()
                QtWidgets.QMessageBox.information(self, "Succès", "Champ personnalisé ajouté avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout : {str(e)}")

    def edit_custom_field(self):
        """Édite le champ personnalisé sélectionné."""
        from club_manager.ui.custom_field_form_dialog import CustomFieldFormDialog
        from club_manager.core.custom_fields import get_all_custom_fields, update_custom_field
        
        selected_items = self.tableCustomFields.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un champ personnalisé à modifier."
            )
            return
        
        row = selected_items[0].row()
        field_id = self.tableCustomFields.item(row, 0).data(Qt.UserRole)
        
        if not field_id:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de récupérer l'ID du champ.")
            return
        
        try:
            fields = get_all_custom_fields()
            field = next((f for f in fields if f['id'] == field_id), None)
            
            if not field:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Champ personnalisé introuvable.")
                return
            
            # Pré-remplir le formulaire
            dlg = CustomFieldFormDialog(self)
            dlg.setWindowTitle("Modifier un champ personnalisé")
            dlg.editName.setText(field.get('name', ''))
            
            if hasattr(dlg, 'comboType'):
                type_index = dlg.comboType.findText(field.get('type', ''))
                if type_index >= 0:
                    dlg.comboType.setCurrentIndex(type_index)
            
            if hasattr(dlg, 'editDefaultValue'):
                dlg.editDefaultValue.setText(field.get('default_value', ''))
            
            if hasattr(dlg, 'editOptions'):
                dlg.editOptions.setText(field.get('options', ''))
            
            if hasattr(dlg, 'editConstraints'):
                dlg.editConstraints.setText(field.get('constraints', ''))
            
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                if not dlg.editName.text():
                    QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le nom du champ est obligatoire.")
                    return
                
                update_custom_field(
                    field_id,
                    name=dlg.editName.text(),
                    ftype=dlg.comboType.currentText() if hasattr(dlg, 'comboType') else 'text',
                    default_value=dlg.editDefaultValue.text() if hasattr(dlg, 'editDefaultValue') else '',
                    options=dlg.editOptions.text() if hasattr(dlg, 'editOptions') else '',
                    constraints=dlg.editConstraints.text() if hasattr(dlg, 'editConstraints') else ''
                )
                self.refresh_custom_fields()
                QtWidgets.QMessageBox.information(self, "Succès", "Champ personnalisé modifié avec succès.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")

    def delete_custom_field(self):
        """Supprime le(s) champ(s) personnalisé(s) sélectionné(s) après confirmation."""
        from club_manager.core.custom_fields import delete_custom_field as delete_field_db
        
        selected_items = self.tableCustomFields.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un ou plusieurs champs personnalisés à supprimer."
            )
            return
        
        selected_rows = set(item.row() for item in selected_items)
        field_count = len(selected_rows)
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer {field_count} champ(s) personnalisé(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    field_id = self.tableCustomFields.item(row, 0).data(Qt.UserRole)
                    if field_id:
                        delete_field_db(field_id)
                
                self.refresh_custom_fields()
                QtWidgets.QMessageBox.information(
                    self,
                    "Succès",
                    f"{field_count} champ(s) personnalisé(s) supprimé(s) avec succès."
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_custom_fields(self):
        """Exporte la liste des champs personnalisés en CSV."""
        from club_manager.core.custom_fields import get_all_custom_fields
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Exporter les champs personnalisés",
            os.path.expanduser("~/champs_personnalises_export.csv"),
            "Fichiers CSV (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            fields = get_all_custom_fields()
            if not fields:
                QtWidgets.QMessageBox.information(self, "Export", "Aucun champ personnalisé à exporter.")
                return
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = fields[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(fields)
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{len(fields)} champ(s) personnalisé(s) exporté(s) vers :\n{file_path}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export : {str(e)}")

    def refresh_custom_fields(self):
        """Recharge la table des champs personnalisés depuis la base de données."""
        from club_manager.core.custom_fields import get_all_custom_fields
        
        fields = get_all_custom_fields()
        self.tableCustomFields.setRowCount(0)
        
        for row_idx, field in enumerate(fields):
            self.tableCustomFields.insertRow(row_idx)
            self.tableCustomFields.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(field['name'] or '')))
            self.tableCustomFields.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(field.get('type', '') or '')))
            self.tableCustomFields.setItem(
                row_idx, 2,
                QtWidgets.QTableWidgetItem(str(field.get('default_value', '') or ''))
            )
            self.tableCustomFields.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(field.get('options', '') or '')))
            self.tableCustomFields.setItem(
                row_idx, 4,
                QtWidgets.QTableWidgetItem(str(field.get('constraints', '') or ''))
            )
            
            # Stocker l'ID avec Qt.UserRole
            self.tableCustomFields.item(row_idx, 0).setData(Qt.UserRole, field['id'])