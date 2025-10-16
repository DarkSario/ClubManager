# -*- coding: utf-8 -*-
"""
Onglet de gestion des prix annuels Club/MJC.
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox, QFormLayout, QCheckBox
from club_manager.core.annual_prices import get_all_annual_prices, add_annual_price, update_annual_price, delete_annual_price, set_current_annual_price

class AnnualPricesTab(QWidget):
    """Onglet de gestion des prix annuels."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.refresh_prices()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout()
        
        # Formulaire d'ajout
        form_layout = QFormLayout()
        
        self.edit_year = QLineEdit()
        self.edit_year.setPlaceholderText("ex: 2024-2025")
        form_layout.addRow(QLabel("Année :"), self.edit_year)
        
        self.edit_club_price = QLineEdit()
        self.edit_club_price.setPlaceholderText("0.00")
        form_layout.addRow(QLabel("Prix Club :"), self.edit_club_price)
        
        self.edit_mjc_price = QLineEdit()
        self.edit_mjc_price.setPlaceholderText("0.00")
        form_layout.addRow(QLabel("Prix MJC :"), self.edit_mjc_price)
        
        self.check_current = QCheckBox("Définir comme année courante")
        form_layout.addRow("", self.check_current)
        
        layout.addLayout(form_layout)
        
        # Bouton d'ajout
        btn_add_layout = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self.add_price)
        btn_add_layout.addWidget(self.btn_add)
        btn_add_layout.addStretch()
        layout.addLayout(btn_add_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Année", "Prix Club", "Prix MJC", "Courante"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.clicked.connect(self.edit_price)
        btn_layout.addWidget(self.btn_edit)
        
        self.btn_set_current = QPushButton("Définir comme courante")
        self.btn_set_current.clicked.connect(self.set_current)
        btn_layout.addWidget(self.btn_set_current)
        
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete_price)
        btn_layout.addWidget(self.btn_delete)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def refresh_prices(self):
        """Rafraîchit la liste des prix."""
        try:
            prices = get_all_annual_prices()
            self.table.setRowCount(len(prices))
            
            for row, price in enumerate(prices):
                id_item = QTableWidgetItem(str(price['id']))
                id_item.setData(QtCore.Qt.UserRole, price['id'])
                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(price['year']))
                self.table.setItem(row, 2, QTableWidgetItem(f"{price['club_price']:.2f} €"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{price['mjc_price']:.2f} €"))
                self.table.setItem(row, 4, QTableWidgetItem("Oui" if price['is_current'] else "Non"))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des prix : {str(e)}")
    
    def add_price(self):
        """Ajoute un nouveau prix annuel."""
        year = self.edit_year.text().strip()
        club_price = self.edit_club_price.text().strip()
        mjc_price = self.edit_mjc_price.text().strip()
        
        if not year or not club_price or not mjc_price:
            QMessageBox.warning(self, "Champs requis", "Veuillez remplir tous les champs.")
            return
        
        try:
            club_price_float = float(club_price)
            mjc_price_float = float(mjc_price)
            
            add_annual_price(year, club_price_float, mjc_price_float, self.check_current.isChecked())
            
            self.edit_year.clear()
            self.edit_club_price.clear()
            self.edit_mjc_price.clear()
            self.check_current.setChecked(False)
            
            self.refresh_prices()
            QMessageBox.information(self, "Succès", "Prix annuel ajouté avec succès.")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Les prix doivent être des nombres valides.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout : {str(e)}")
    
    def edit_price(self):
        """Modifie le prix sélectionné."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un prix à modifier.")
            return
        
        row = selected_items[0].row()
        price_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        
        # Récupérer les valeurs actuelles
        current_year = self.table.item(row, 1).text()
        current_club = self.table.item(row, 2).text().replace(" €", "")
        current_mjc = self.table.item(row, 3).text().replace(" €", "")
        is_current = self.table.item(row, 4).text() == "Oui"
        
        # Dialogue de modification
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Modifier le prix annuel")
        dialog_layout = QFormLayout()
        
        edit_year = QLineEdit(current_year)
        dialog_layout.addRow("Année :", edit_year)
        
        edit_club_price = QLineEdit(current_club)
        dialog_layout.addRow("Prix Club :", edit_club_price)
        
        edit_mjc_price = QLineEdit(current_mjc)
        dialog_layout.addRow("Prix MJC :", edit_mjc_price)
        
        check_current = QCheckBox("Année courante")
        check_current.setChecked(is_current)
        dialog_layout.addRow("", check_current)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addRow(buttons)
        
        dialog.setLayout(dialog_layout)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                update_annual_price(
                    price_id,
                    edit_year.text(),
                    float(edit_club_price.text()),
                    float(edit_mjc_price.text()),
                    check_current.isChecked()
                )
                self.refresh_prices()
                QMessageBox.information(self, "Succès", "Prix annuel modifié avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")
    
    def set_current(self):
        """Définit le prix sélectionné comme courant."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un prix.")
            return
        
        row = selected_items[0].row()
        price_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        
        try:
            set_current_annual_price(price_id)
            self.refresh_prices()
            QMessageBox.information(self, "Succès", "Prix défini comme courant.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")
    
    def delete_price(self):
        """Supprime le prix sélectionné."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un prix à supprimer.")
            return
        
        row = selected_items[0].row()
        price_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        year = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer le prix de l'année '{year}' ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_annual_price(price_id)
                self.refresh_prices()
                QMessageBox.information(self, "Succès", "Prix annuel supprimé avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")
