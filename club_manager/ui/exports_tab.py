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

class ExportsTab(QtWidgets.QWidget, Ui_ExportsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonExportCSV.clicked.connect(self.export_csv)
        self.buttonExportPDF.clicked.connect(self.export_pdf)
        self.buttonSelectFields.clicked.connect(self.select_fields)

    def export_csv(self):
        # Exporter les données en CSV
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        import csv
        
        # Demander quel type de données exporter
        items = ["Membres", "Cotisations", "Postes"]
        item, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Type d'export",
            "Sélectionnez le type de données à exporter:",
            items,
            0,
            False
        )
        
        if not ok:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en CSV",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                if item == "Membres":
                    from club_manager.core.members import get_all_members
                    members = get_all_members()
                    
                    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['ID', 'Nom', 'Prénom', 'Adresse', 'Code Postal', 'Ville', 'Téléphone', 'Email', 'RGPD', 'Droits Image', 'Total Payé']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for member in members:
                            writer.writerow({
                                'ID': member['id'],
                                'Nom': member['last_name'] or '',
                                'Prénom': member['first_name'] or '',
                                'Adresse': member['address'] or '',
                                'Code Postal': member['postal_code'] or '',
                                'Ville': member['city'] or '',
                                'Téléphone': member['phone'] or '',
                                'Email': member['mail'] or '',
                                'RGPD': 'Oui' if member['rgpd'] else 'Non',
                                'Droits Image': 'Oui' if member['image_rights'] else 'Non',
                                'Total Payé': member['total_paid'] or '0'
                            })
                
                elif item == "Cotisations":
                    from club_manager.core.cotisations import get_all_cotisations
                    from club_manager.core.members import get_member_by_id
                    
                    cotisations = get_all_cotisations()
                    
                    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['ID', 'Membre', 'Montant', 'Payé', 'Date', 'Méthode', 'Statut']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for cotisation in cotisations:
                            try:
                                member = get_member_by_id(cotisation['member_id'])
                                member_name = f"{member['last_name']} {member['first_name']}" if member else "Inconnu"
                            except:
                                member_name = "Inconnu"
                            
                            writer.writerow({
                                'ID': cotisation['id'],
                                'Membre': member_name,
                                'Montant': cotisation['amount'] or '0',
                                'Payé': cotisation['paid'] or '0',
                                'Date': cotisation['payment_date'] or '',
                                'Méthode': cotisation['method'] or '',
                                'Statut': cotisation['status'] or ''
                            })
                
                elif item == "Postes":
                    from club_manager.core.positions import get_all_positions
                    from club_manager.core.members import get_member_by_id
                    
                    positions = get_all_positions()
                    
                    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['ID', 'Nom', 'Type', 'Description', 'Affecté à']
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
                                'ID': position['id'],
                                'Nom': position['name'] or '',
                                'Type': position['type'] or '',
                                'Description': position['description'] or '',
                                'Affecté à': assigned_to
                            })
                
                QMessageBox.information(self, "Succès", f"Export CSV réussi vers {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def export_pdf(self):
        # Exporter les données en PDF
        QtWidgets.QMessageBox.information(
            self,
            "Export PDF",
            "L'export PDF nécessite une bibliothèque additionnelle (ex: reportlab).\n"
            "Veuillez utiliser l'export CSV pour le moment."
        )

    def select_fields(self):
        # Ouvrir un dialog pour sélectionner les champs à exporter
        from club_manager.ui.export_fields_dialog import ExportFieldsDialog
        
        dlg = ExportFieldsDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            QtWidgets.QMessageBox.information(
                self,
                "Champs sélectionnés",
                "La personnalisation des champs à exporter sera implémentée prochainement."
            )