# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/custom_fields_tab.py
Rôle : Onglet gestion des champs personnalisés (CustomFieldsTab) du Club Manager.
Hérite de QWidget et de Ui_CustomFieldsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CustomFieldsTab généré par pyuic5 à partir de resources/ui/custom_fields_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.custom_fields_tab_ui import Ui_CustomFieldsTab

class CustomFieldsTab(QtWidgets.QWidget, Ui_CustomFieldsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddCustomField.clicked.connect(self.add_custom_field)
        self.buttonEditCustomField.clicked.connect(self.edit_custom_field)
        self.buttonDeleteCustomField.clicked.connect(self.delete_custom_field)
        self.buttonExportCustomFields.clicked.connect(self.export_custom_fields)
        self.tableCustomFields.doubleClicked.connect(self.edit_custom_field)
        # Charger les champs personnalisés au démarrage
        try:
            self.refresh_custom_fields()
        except:
            pass

    def add_custom_field(self):
        from club_manager.ui.custom_field_form_dialog import CustomFieldFormDialog
        dlg = CustomFieldFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_custom_fields()

    def edit_custom_field(self):
        # Logique de modification du champ personnalisé sélectionné
        selected_rows = self.tableCustomFields.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner un champ personnalisé à modifier.")
            return
        
        QtWidgets.QMessageBox.information(
            self,
            "Modification",
            "La modification de champ personnalisé nécessite une refonte du formulaire.\n"
            "Veuillez supprimer et recréer le champ."
        )

    def delete_custom_field(self):
        # Logique de suppression du/des champs personnalisés sélectionnés
        selected_rows = self.tableCustomFields.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un champ personnalisé à supprimer.")
            return
        
        # Demander confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer {len(selected_rows)} champ(s) personnalisé(s) ?\nCette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            from club_manager.core.custom_fields import delete_custom_field as delete_custom_field_db
            try:
                for row in selected_rows:
                    field_id = self.tableCustomFields.item(row.row(), 0).data(QtWidgets.QTableWidgetItem.UserType)
                    delete_custom_field_db(field_id)
                
                # Recharger la table
                self.refresh_custom_fields()
                QtWidgets.QMessageBox.information(self, "Succès", f"{len(selected_rows)} champ(s) personnalisé(s) supprimé(s) avec succès.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def export_custom_fields(self):
        # Exporter les champs personnalisés
        from PyQt5.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les champs personnalisés",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                from club_manager.core.custom_fields import get_all_custom_fields
                
                custom_fields = get_all_custom_fields()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nom', 'Type', 'Valeur par défaut', 'Options', 'Contraintes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for field in custom_fields:
                        writer.writerow({
                            'Nom': field['name'] or '',
                            'Type': field['type'] or '',
                            'Valeur par défaut': field['default_value'] or '',
                            'Options': field['options'] or '',
                            'Contraintes': field['constraints'] or ''
                        })
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Export réussi vers {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def refresh_custom_fields(self):
        # Recharge la table depuis la base
        from club_manager.core.custom_fields import get_all_custom_fields
        
        custom_fields = get_all_custom_fields()
        self.tableCustomFields.setRowCount(0)
        
        for row_idx, field in enumerate(custom_fields):
            self.tableCustomFields.insertRow(row_idx)
            
            # Nom
            self.tableCustomFields.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(field['name'] or '')))
            
            # Type
            self.tableCustomFields.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(field['type'] or '')))
            
            # Valeur par défaut
            self.tableCustomFields.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(field['default_value'] or '')))
            
            # Options
            self.tableCustomFields.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(field['options'] or '')))
            
            # Contraintes
            self.tableCustomFields.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(field['constraints'] or '')))
            
            # Stocker l'ID
            self.tableCustomFields.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, field['id'])