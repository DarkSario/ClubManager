# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/csv_export_dialog.py
Rôle : Dialogue de configuration des exports CSV avec sélection du séparateur.
"""

from PyQt5 import QtWidgets, QtCore

class CSVExportDialog(QtWidgets.QDialog):
    """Dialogue pour configurer les options d'export CSV."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options d'export CSV")
        self.resize(500, 250)
        
        # Valeurs par défaut
        self.delimiter = ';'
        self.add_bom = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialise l'interface utilisateur."""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Groupe pour le séparateur
        separator_group = QtWidgets.QGroupBox("Séparateur de colonnes")
        separator_layout = QtWidgets.QVBoxLayout()
        
        # Options de séparateur
        self.radio_semicolon = QtWidgets.QRadioButton("Point-virgule (;) - Recommandé pour Excel France")
        self.radio_comma = QtWidgets.QRadioButton("Virgule (,) - Standard international")
        self.radio_tab = QtWidgets.QRadioButton("Tabulation (\\t) - Pour import avancé")
        
        # Point-virgule par défaut (France)
        self.radio_semicolon.setChecked(True)
        
        separator_layout.addWidget(self.radio_semicolon)
        separator_layout.addWidget(self.radio_comma)
        separator_layout.addWidget(self.radio_tab)
        
        separator_group.setLayout(separator_layout)
        layout.addWidget(separator_group)
        
        # Groupe pour les options avancées
        options_group = QtWidgets.QGroupBox("Options avancées")
        options_layout = QtWidgets.QVBoxLayout()
        
        self.checkbox_bom = QtWidgets.QCheckBox(
            "Ajouter BOM UTF-8 (pour Excel Windows qui ne détecte pas l'UTF-8)"
        )
        self.checkbox_bom.setChecked(False)
        
        options_layout.addWidget(self.checkbox_bom)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Zone d'information
        info_label = QtWidgets.QLabel(
            "<b>Compatibilité :</b><br>"
            "• <b>Point-virgule (;)</b> : Idéal pour Excel français et LibreOffice en France<br>"
            "• <b>Virgule (,)</b> : Standard pour Excel anglais et applications internationales<br>"
            "• <b>Tabulation</b> : Pour import dans des outils techniques<br><br>"
            "<i>Les guillemets et caractères spéciaux sont automatiquement gérés.</i>"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }")
        layout.addWidget(info_label)
        
        # Boutons OK/Annuler
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def accept(self):
        """Appelé quand l'utilisateur clique sur OK."""
        # Récupérer le séparateur choisi
        if self.radio_semicolon.isChecked():
            self.delimiter = ';'
        elif self.radio_comma.isChecked():
            self.delimiter = ','
        elif self.radio_tab.isChecked():
            self.delimiter = '\t'
        
        # Récupérer l'option BOM
        self.add_bom = self.checkbox_bom.isChecked()
        
        super().accept()
    
    def get_options(self):
        """
        Retourne les options d'export choisies.
        
        Returns:
            dict: Dictionnaire avec 'delimiter' et 'add_bom'
        """
        return {
            'delimiter': self.delimiter,
            'add_bom': self.add_bom
        }
