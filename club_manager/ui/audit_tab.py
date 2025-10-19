# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/audit_tab.py
Rôle : Onglet audit (AuditTab) du Club Manager.
Hérite de QWidget et de Ui_AuditTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_AuditTab généré par pyuic5 à partir de resources/ui/audit_tab.ui
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from club_manager.ui.audit_tab_ui import Ui_AuditTab
import csv
import os

class AuditTab(QtWidgets.QWidget, Ui_AuditTab):
    """Onglet de consultation du journal d'audit et gestion RGPD."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.buttonExportAudit.clicked.connect(self.export_audit)
        self.buttonPurgeRGPD.clicked.connect(self.purge_rgpd)
        self.tableAudit.doubleClicked.connect(self.view_audit_entry)
        
        # Charger au démarrage
        try:
            self.refresh_audit()
        except:
            pass

    def export_audit(self):
        """Exporte le journal d'audit en CSV."""
        from club_manager.core.audit import get_all_audit_entries
        from club_manager.ui.csv_export_dialog import CSVExportDialog
        from club_manager.core.exports import export_to_csv
        
        try:
            entries = get_all_audit_entries()
            if not entries:
                QtWidgets.QMessageBox.information(self, "Export", "Aucune entrée d'audit à exporter.")
                return
            
            # Demander les options d'export CSV
            csv_dialog = CSVExportDialog(self)
            if csv_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            
            options = csv_dialog.get_options()
            
            # Demander le chemin de sauvegarde
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Exporter le journal d'audit",
                os.path.expanduser("~/audit_export.csv"),
                "Fichiers CSV (*.csv)"
            )
            
            if not file_path:
                return
            
            # Utiliser la fonction d'export centralisée avec les options choisies
            num_rows = export_to_csv(
                entries,
                file_path,
                delimiter=options['delimiter'],
                add_bom=options['add_bom'],
                translate_headers=True
            )
            
            separator_name = {';': 'point-virgule', ',': 'virgule', '\t': 'tabulation'}
            
            QtWidgets.QMessageBox.information(
                self,
                "Export réussi",
                f"{num_rows} entrée(s) d'audit exportée(s) vers :\n{file_path}\n\n"
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

    def purge_rgpd(self):
        """Lance la procédure de purge/anonymisation RGPD."""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Purge RGPD",
            "La purge RGPD supprime ou anonymise les données personnelles anciennes.\n\n"
            "Cette action est irréversible. Continuer ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QMessageBox.information(
                self,
                "Purge RGPD",
                "La fonctionnalité de purge RGPD sera disponible dans une prochaine version.\n\n"
                "Elle permettra de :\n"
                "- Supprimer les membres inactifs depuis X années\n"
                "- Anonymiser les données sensibles\n"
                "- Purger l'historique d'audit ancien"
            )

    def view_audit_entry(self):
        """Affiche le détail d'une entrée d'audit."""
        selected_items = self.tableAudit.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        
        # Récupérer les informations de la ligne
        date = self.tableAudit.item(row, 0).text() if self.tableAudit.item(row, 0) else ""
        action = self.tableAudit.item(row, 1).text() if self.tableAudit.item(row, 1) else ""
        user = self.tableAudit.item(row, 2).text() if self.tableAudit.item(row, 2) else ""
        obj = self.tableAudit.item(row, 3).text() if self.tableAudit.item(row, 3) else ""
        details = self.tableAudit.item(row, 4).text() if self.tableAudit.item(row, 4) else ""
        
        # Afficher dans une boîte de dialogue
        msg_text = f"<h3>Détails de l'entrée d'audit</h3>"
        msg_text += f"<p><b>Date :</b> {date}</p>"
        msg_text += f"<p><b>Action :</b> {action}</p>"
        msg_text += f"<p><b>Utilisateur :</b> {user}</p>"
        msg_text += f"<p><b>Objet :</b> {obj}</p>"
        msg_text += f"<p><b>Détails :</b> {details}</p>"
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Détails de l'audit")
        msg.setTextFormat(Qt.RichText)
        msg.setText(msg_text)
        msg.exec_()

    def refresh_audit(self):
        """Recharge la table d'audit depuis la base de données."""
        from club_manager.core.audit import get_all_audit_entries
        
        entries = get_all_audit_entries()
        self.tableAudit.setRowCount(0)
        
        for row_idx, entry in enumerate(entries):
            self.tableAudit.insertRow(row_idx)
            self.tableAudit.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(entry.get('date', ''))))
            self.tableAudit.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(entry.get('action', ''))))
            self.tableAudit.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(entry.get('user', ''))))
            self.tableAudit.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(entry.get('object', ''))))
            self.tableAudit.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(str(entry.get('details', ''))))