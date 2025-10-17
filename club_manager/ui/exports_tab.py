# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/exports_tab.py
Rôle : Onglet exports (ExportsTab) du Club Manager.
Hérite de QWidget et de Ui_ExportsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ExportsTab généré par pyuic5 à partir de resources/ui/exports_tab.ui
"""

from PyQt5 import QtWidgets, QtCore
from club_manager.ui.exports_tab_ui import Ui_ExportsTab
from club_manager.core.export import get_french_field_name
import csv
import os

class ExportsTab(QtWidgets.QWidget, Ui_ExportsTab):
    """Onglet d'export avancé avec sélection de champs et formats."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonExportCSV.clicked.connect(self.export_csv)
        self.buttonExportPDF.clicked.connect(self.export_pdf)
        self.buttonSelectFields.clicked.connect(self.select_fields)

    def export_csv(self):
        """Exporte les données sélectionnées en CSV."""
        from club_manager.core.members import get_all_members
        
        # Demander quel type de données exporter
        choice, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Type d'export",
            "Que souhaitez-vous exporter ?",
            ["Membres", "Postes", "Clubs MJC", "Prix annuels"],
            0,
            False
        )
        
        if not ok:
            return
        
        try:
            data = []
            filename = ""
            
            if choice == "Membres":
                from club_manager.core.members import get_all_members
                data = get_all_members()
                filename = "membres_export.csv"
            elif choice == "Postes":
                from club_manager.core.positions import get_all_positions
                data = get_all_positions()
                filename = "postes_export.csv"
            elif choice == "Clubs MJC":
                from club_manager.core.mjc_clubs import get_all_mjc_clubs
                data = get_all_mjc_clubs()
                filename = "clubs_mjc_export.csv"
            elif choice == "Prix annuels":
                from club_manager.core.annual_prices import get_all_annual_prices
                data = get_all_annual_prices()
                filename = "prix_annuels_export.csv"
            
            if not data:
                QtWidgets.QMessageBox.information(self, "Export", f"Aucune donnée à exporter pour {choice}.")
                return
            
            # Demander le chemin de sauvegarde
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                f"Exporter {choice}",
                os.path.expanduser(f"~/{filename}"),
                "Fichiers CSV (*.csv)"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    # Convert sqlite3.Row objects to dicts for CSV export
                    data_list = [dict(row) for row in data]
                    fieldnames = data_list[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data_list)
                
                QtWidgets.QMessageBox.information(
                    self,
                    "Export réussi",
                    f"{len(data)} ligne(s) exportée(s) vers :\n{file_path}"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export : {str(e)}")

    def export_pdf(self):
        """Exporte les données en PDF avec possibilité de sélectionner les champs."""
        from club_manager.core.export import export_to_pdf
        
        # Demander quel type de données exporter
        choice, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Type d'export PDF",
            "Que souhaitez-vous exporter ?",
            ["Membres", "Postes", "Clubs MJC", "Prix annuels"],
            0,
            False
        )
        
        if not ok:
            return
        
        try:
            data = []
            
            if choice == "Membres":
                from club_manager.core.members import get_all_members
                data = get_all_members()
            elif choice == "Postes":
                from club_manager.core.positions import get_all_positions
                data = get_all_positions()
            elif choice == "Clubs MJC":
                from club_manager.core.mjc_clubs import get_all_mjc_clubs
                data = get_all_mjc_clubs()
            elif choice == "Prix annuels":
                from club_manager.core.annual_prices import get_all_annual_prices
                data = get_all_annual_prices()
            
            if not data:
                QtWidgets.QMessageBox.information(self, "Export PDF", f"Aucune donnée à exporter pour {choice}.")
                return
            
            # Demander si l'utilisateur veut sélectionner les champs
            reply = QtWidgets.QMessageBox.question(
                self,
                "Sélection des champs",
                "Voulez-vous sélectionner les champs à exporter ?\n\n"
                "Oui : Sélectionner les champs spécifiques\n"
                "Non : Exporter tous les champs",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            selected_fields = None
            if reply == QtWidgets.QMessageBox.Yes:
                selected_fields = self._select_export_fields(data[0].keys())
                if not selected_fields:
                    return
            
            # Exporter en PDF
            export_to_pdf(data, choice, selected_fields, parent=self)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d'export PDF", f"Erreur lors de l'export : {str(e)}")
    
    def _select_export_fields(self, available_fields):
        """Ouvre un dialogue pour sélectionner les champs à exporter."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sélectionner les champs à exporter")
        dialog.resize(400, 500)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        label = QtWidgets.QLabel("Sélectionnez les champs à inclure dans l'export :")
        layout.addWidget(label)
        
        # Liste des champs avec checkboxes
        list_widget = QtWidgets.QListWidget()
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        
        for field in available_fields:
            # Utiliser la traduction française du nom du champ
            display_name = get_french_field_name(field)
            item = QtWidgets.QListWidgetItem(display_name)
            item.setData(QtCore.Qt.UserRole, field)
            list_widget.addItem(item)
            # Sélectionner par défaut
            item.setSelected(True)
        
        layout.addWidget(list_widget)
        
        # Boutons de sélection rapide
        btn_layout = QtWidgets.QHBoxLayout()
        btn_select_all = QtWidgets.QPushButton("Tout sélectionner")
        btn_select_all.clicked.connect(list_widget.selectAll)
        btn_layout.addWidget(btn_select_all)
        
        btn_deselect_all = QtWidgets.QPushButton("Tout désélectionner")
        btn_deselect_all.clicked.connect(list_widget.clearSelection)
        btn_layout.addWidget(btn_deselect_all)
        
        layout.addLayout(btn_layout)
        
        # Boutons OK/Annuler
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected = [item.data(QtCore.Qt.UserRole) for item in list_widget.selectedItems()]
            return selected if selected else None
        
        return None

    def select_fields(self):
        """Ouvre un dialogue pour sélectionner les champs à exporter."""
        QtWidgets.QMessageBox.information(
            self,
            "Sélection de champs",
            "La sélection de champs personnalisés sera disponible dans une prochaine version.\n"
            "Actuellement, tous les champs sont exportés par défaut."
        )