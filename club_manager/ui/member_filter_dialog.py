# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/member_filter_dialog.py
Rôle : Dialogue de filtrage des membres avec divers critères
"""

from PyQt5 import QtWidgets, QtCore


class MemberFilterDialog(QtWidgets.QDialog):
    """Dialogue pour saisir les critères de filtrage des membres."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filtrer les membres")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur du dialogue."""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Label d'instructions
        label_info = QtWidgets.QLabel(
            "Saisissez les critères de recherche. Laissez vide pour ignorer un critère."
        )
        label_info.setWordWrap(True)
        layout.addWidget(label_info)
        
        # Groupe pour les filtres de texte
        group_text = QtWidgets.QGroupBox("Recherche textuelle")
        form_text = QtWidgets.QFormLayout()
        
        self.edit_last_name = QtWidgets.QLineEdit()
        self.edit_last_name.setPlaceholderText("Saisissez un nom...")
        form_text.addRow("Nom :", self.edit_last_name)
        
        self.edit_first_name = QtWidgets.QLineEdit()
        self.edit_first_name.setPlaceholderText("Saisissez un prénom...")
        form_text.addRow("Prénom :", self.edit_first_name)
        
        self.edit_city = QtWidgets.QLineEdit()
        self.edit_city.setPlaceholderText("Saisissez une ville...")
        form_text.addRow("Ville :", self.edit_city)
        
        self.edit_mail = QtWidgets.QLineEdit()
        self.edit_mail.setPlaceholderText("Saisissez un email...")
        form_text.addRow("Email :", self.edit_mail)
        
        group_text.setLayout(form_text)
        layout.addWidget(group_text)
        
        # Groupe pour les filtres de statut
        group_status = QtWidgets.QGroupBox("Statuts")
        form_status = QtWidgets.QFormLayout()
        
        self.combo_cotisation_status = QtWidgets.QComboBox()
        self.combo_cotisation_status.addItems([
            "Tous",
            "Payée",
            "Non payée",
            "Partiellement payée"
        ])
        form_status.addRow("Statut cotisation :", self.combo_cotisation_status)
        
        self.combo_payment_type = QtWidgets.QComboBox()
        self.combo_payment_type.addItems([
            "Tous",
            "Club + MJC",
            "Club uniquement"
        ])
        form_status.addRow("Type de paiement :", self.combo_payment_type)
        
        group_status.setLayout(form_status)
        layout.addWidget(group_status)
        
        # Groupe pour les consentements
        group_consent = QtWidgets.QGroupBox("Consentements")
        form_consent = QtWidgets.QFormLayout()
        
        self.combo_rgpd = QtWidgets.QComboBox()
        self.combo_rgpd.addItems(["Tous", "Oui", "Non"])
        form_consent.addRow("RGPD :", self.combo_rgpd)
        
        self.combo_image_rights = QtWidgets.QComboBox()
        self.combo_image_rights.addItems(["Tous", "Oui", "Non"])
        form_consent.addRow("Droit à l'image :", self.combo_image_rights)
        
        group_consent.setLayout(form_consent)
        layout.addWidget(group_consent)
        
        # Boutons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Bouton pour réinitialiser
        btn_reset = QtWidgets.QPushButton("Réinitialiser")
        btn_reset.clicked.connect(self.reset_filters)
        button_box.addButton(btn_reset, QtWidgets.QDialogButtonBox.ResetRole)
        
        layout.addWidget(button_box)
    
    def reset_filters(self):
        """Réinitialise tous les filtres."""
        self.edit_last_name.clear()
        self.edit_first_name.clear()
        self.edit_city.clear()
        self.edit_mail.clear()
        self.combo_cotisation_status.setCurrentIndex(0)
        self.combo_payment_type.setCurrentIndex(0)
        self.combo_rgpd.setCurrentIndex(0)
        self.combo_image_rights.setCurrentIndex(0)
    
    def get_filters(self):
        """
        Retourne un dictionnaire des filtres actifs.
        
        Returns:
            dict: Dictionnaire des filtres avec les valeurs saisies
        """
        filters = {}
        
        # Filtres texte
        if self.edit_last_name.text().strip():
            filters['last_name'] = self.edit_last_name.text().strip()
        
        if self.edit_first_name.text().strip():
            filters['first_name'] = self.edit_first_name.text().strip()
        
        if self.edit_city.text().strip():
            filters['city'] = self.edit_city.text().strip()
        
        if self.edit_mail.text().strip():
            filters['mail'] = self.edit_mail.text().strip()
        
        # Filtres de statut
        if self.combo_cotisation_status.currentText() != "Tous":
            filters['cotisation_status'] = self.combo_cotisation_status.currentText()
        
        if self.combo_payment_type.currentText() != "Tous":
            payment_type_map = {
                "Club + MJC": "club_mjc",
                "Club uniquement": "club_only"
            }
            filters['payment_type'] = payment_type_map[self.combo_payment_type.currentText()]
        
        # Filtres de consentement
        if self.combo_rgpd.currentText() != "Tous":
            filters['rgpd'] = 1 if self.combo_rgpd.currentText() == "Oui" else 0
        
        if self.combo_image_rights.currentText() != "Tous":
            filters['image_rights'] = 1 if self.combo_image_rights.currentText() == "Oui" else 0
        
        return filters
