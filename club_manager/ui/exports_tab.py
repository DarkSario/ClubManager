# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/exports_tab.py
Rôle : Onglet exports (ExportsTab) du Club Manager.
Hérite de QWidget et de Ui_ExportsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ExportsTab généré par pyuic5 à partir de resources/ui/exports_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.exports_tab_ui import Ui_ExportsTab
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
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                
                QtWidgets.QMessageBox.information(
                    self,
                    "Export réussi",
                    f"{len(data)} ligne(s) exportée(s) vers :\n{file_path}"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export : {str(e)}")

    def export_pdf(self):
        """Exporte les données en PDF (fonctionnalité à implémenter)."""
        QtWidgets.QMessageBox.information(
            self,
            "Export PDF",
            "L'export PDF sera disponible dans une prochaine version.\n"
            "Utilisez l'export CSV en attendant."
        )

    def select_fields(self):
        """Ouvre un dialogue pour sélectionner les champs à exporter."""
        QtWidgets.QMessageBox.information(
            self,
            "Sélection de champs",
            "La sélection de champs personnalisés sera disponible dans une prochaine version.\n"
            "Actuellement, tous les champs sont exportés par défaut."
        )