# -*- coding: utf-8 -*-
"""
Onglet de gestion des clubs MJC.
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox
from club_manager.core.mjc_clubs import get_all_mjc_clubs, add_mjc_club, update_mjc_club, delete_mjc_club

class MJCClubsTab(QWidget):
    """Onglet de gestion des clubs MJC."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.refresh_clubs()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout()
        
        # Formulaire d'ajout
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Nom du club MJC :"))
        self.edit_club_name = QLineEdit()
        form_layout.addWidget(self.edit_club_name)
        
        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self.add_club)
        form_layout.addWidget(self.btn_add)
        
        self.btn_import = QPushButton("Importer/Coller une liste")
        self.btn_import.clicked.connect(self.import_clubs_list)
        form_layout.addWidget(self.btn_import)
        
        layout.addLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nom du club"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.clicked.connect(self.edit_club)
        btn_layout.addWidget(self.btn_edit)
        
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete_club)
        btn_layout.addWidget(self.btn_delete)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def refresh_clubs(self):
        """Rafraîchit la liste des clubs."""
        try:
            clubs = get_all_mjc_clubs()
            self.table.setRowCount(len(clubs))
            
            for row, club in enumerate(clubs):
                id_item = QTableWidgetItem(str(club['id']))
                id_item.setData(QtCore.Qt.UserRole, club['id'])
                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(club['name']))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des clubs : {str(e)}")
    
    def add_club(self):
        """Ajoute un nouveau club MJC."""
        name = self.edit_club_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Champ requis", "Veuillez saisir un nom de club.")
            return
        
        try:
            add_mjc_club(name)
            self.edit_club_name.clear()
            self.refresh_clubs()
            QMessageBox.information(self, "Succès", "Club MJC ajouté avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout : {str(e)}")
    
    def edit_club(self):
        """Modifie le club sélectionné."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un club à modifier.")
            return
        
        row = selected_items[0].row()
        club_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        current_name = self.table.item(row, 1).text()
        
        name, ok = QtWidgets.QInputDialog.getText(self, "Modifier le club", "Nom du club :", text=current_name)
        if ok and name:
            try:
                update_mjc_club(club_id, name)
                self.refresh_clubs()
                QMessageBox.information(self, "Succès", "Club MJC modifié avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")
    
    def delete_club(self):
        """Supprime le club sélectionné."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un club à supprimer.")
            return
        
        row = selected_items[0].row()
        club_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        club_name = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer le club '{club_name}' ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_mjc_club(club_id)
                self.refresh_clubs()
                QMessageBox.information(self, "Succès", "Club MJC supprimé avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")
    
    def import_clubs_list(self):
        """Importe ou colle une liste de clubs MJC."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Importer une liste de clubs MJC")
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Instructions
        instructions = QLabel(
            "Collez la liste des clubs MJC (un par ligne) ou importez depuis un fichier texte.\n"
            "Les doublons seront ignorés automatiquement."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Zone de texte
        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlaceholderText("MJC Centre\nMJC Nord\nMJC Sud\n...")
        layout.addWidget(text_edit)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        btn_load_file = QPushButton("Charger depuis un fichier")
        btn_load_file.clicked.connect(lambda: self._load_clubs_from_file(text_edit))
        btn_layout.addWidget(btn_load_file)
        
        btn_layout.addStretch()
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        btn_layout.addWidget(buttons)
        
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            clubs_text = text_edit.toPlainText().strip()
            if not clubs_text:
                QMessageBox.warning(self, "Liste vide", "Veuillez saisir au moins un club.")
                return
            
            # Parser la liste (un club par ligne)
            club_names = [line.strip() for line in clubs_text.split('\n') if line.strip()]
            
            # Récupérer les clubs existants pour éviter les doublons
            existing_clubs = get_all_mjc_clubs()
            existing_names = {club['name'].lower() for club in existing_clubs}
            
            # Ajouter les nouveaux clubs
            added_count = 0
            skipped_count = 0
            errors = []
            
            for name in club_names:
                if name.lower() in existing_names:
                    skipped_count += 1
                    continue
                
                try:
                    add_mjc_club(name)
                    existing_names.add(name.lower())
                    added_count += 1
                except Exception as e:
                    errors.append(f"{name}: {str(e)}")
            
            # Rafraîchir la liste
            self.refresh_clubs()
            
            # Afficher le résultat
            message = f"{added_count} club(s) ajouté(s).\n{skipped_count} club(s) ignoré(s) (doublons)."
            if errors:
                message += f"\n\nErreurs :\n" + "\n".join(errors)
            
            if errors:
                QMessageBox.warning(self, "Import terminé avec erreurs", message)
            else:
                QMessageBox.information(self, "Import réussi", message)
    
    def _load_clubs_from_file(self, text_edit):
        """Charge les clubs depuis un fichier texte."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier texte",
            "",
            "Fichiers texte (*.txt);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                text_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la lecture du fichier : {str(e)}")
