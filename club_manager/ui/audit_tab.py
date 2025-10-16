# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/audit_tab.py
Rôle : Onglet audit (AuditTab) du Club Manager.
Hérite de QWidget et de Ui_AuditTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_AuditTab généré par pyuic5 à partir de resources/ui/audit_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.audit_tab_ui import Ui_AuditTab

class AuditTab(QtWidgets.QWidget, Ui_AuditTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonExportAudit.clicked.connect(self.export_audit)
        self.buttonPurgeRGPD.clicked.connect(self.purge_rgpd)
        self.tableAudit.doubleClicked.connect(self.view_audit_entry)
        # Charger l'audit au démarrage
        try:
            self.refresh_audit()
        except:
            pass

    def export_audit(self):
        # Exporter le journal d'audit (CSV/PDF)
        from PyQt5.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le journal d'audit",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                from club_manager.core.audit import get_all_audit_entries
                
                audit_entries = get_all_audit_entries()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['ID', 'Date', 'Action', 'Utilisateur', 'Objet', 'Détails']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for entry in audit_entries:
                        writer.writerow({
                            'ID': entry['id'],
                            'Date': entry['date'] or '',
                            'Action': entry['action'] or '',
                            'Utilisateur': entry['user'] or '',
                            'Objet': entry['object'] or '',
                            'Détails': entry['details'] or ''
                        })
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Export réussi vers {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export : {str(e)}")

    def purge_rgpd(self):
        # Lancer la purge RGPD (suppression/anonymisation)
        from club_manager.ui.rgpd_purge_dialog import RGPDPurgeDialog
        
        try:
            dlg = RGPDPurgeDialog(self)
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                QtWidgets.QMessageBox.information(
                    self,
                    "Purge RGPD",
                    "La purge RGPD a été effectuée avec succès."
                )
                self.refresh_audit()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la purge RGPD : {str(e)}")

    def view_audit_entry(self):
        # Afficher le détail d'une entrée d'audit
        selected_rows = self.tableAudit.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez sélectionner une entrée d'audit.")
            return
        
        from club_manager.ui.audit_details_dialog import AuditDetailsDialog
        
        try:
            row = selected_rows[0].row()
            audit_id = self.tableAudit.item(row, 0).data(QtWidgets.QTableWidgetItem.UserType)
            
            dlg = AuditDetailsDialog(self, audit_id)
            dlg.exec_()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage du détail : {str(e)}")

    def refresh_audit(self):
        # Recharge la table depuis la base
        from club_manager.core.audit import get_all_audit_entries
        
        audit_entries = get_all_audit_entries()
        self.tableAudit.setRowCount(0)
        
        for row_idx, entry in enumerate(audit_entries):
            self.tableAudit.insertRow(row_idx)
            
            # Date
            self.tableAudit.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(entry['date'] or '')))
            
            # Action
            self.tableAudit.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(entry['action'] or '')))
            
            # Utilisateur
            self.tableAudit.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(entry['user'] or '')))
            
            # Objet
            self.tableAudit.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(entry['object'] or '')))
            
            # Détails
            details = str(entry['details'] or '')[:100]  # Limiter à 100 caractères
            self.tableAudit.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(details))
            
            # Stocker l'ID
            self.tableAudit.item(row_idx, 0).setData(QtWidgets.QTableWidgetItem.UserType, entry['id'])