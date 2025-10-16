# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/theming_tab.py
Rôle : Onglet thématisation (ThemingTab) du Club Manager.
Hérite de QWidget et de Ui_ThemingTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ThemingTab généré par pyuic5 à partir de resources/ui/theming_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.theming_tab_ui import Ui_ThemingTab
from club_manager.core.theming import load_theme, import_logo as import_logo_core, save_theme_choice
import os

class ThemingTab(QtWidgets.QWidget, Ui_ThemingTab):
    """Onglet de personnalisation du thème et du logo."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._current_qss = None
        self._current_logo = None
        
        self.buttonChooseTheme.clicked.connect(self.choose_theme)
        self.buttonImportLogo.clicked.connect(self.import_logo)
        self.buttonPreviewTheme.clicked.connect(self.preview_theme)

    def choose_theme(self):
        """Permet de choisir un fichier QSS pour personnaliser l'interface."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier de thème",
            os.path.expanduser("~/"),
            "Fichiers QSS (*.qss);;Tous les fichiers (*.*)"
        )
        
        if file_path:
            self._current_qss = file_path
            QtWidgets.QMessageBox.information(
                self,
                "Thème sélectionné",
                f"Thème sélectionné : {os.path.basename(file_path)}\n\n"
                "Cliquez sur 'Prévisualiser le thème' pour l'appliquer."
            )

    def import_logo(self):
        """Permet d'importer un logo personnalisé."""
        logo_path = import_logo_core(self)
        
        if logo_path:
            self._current_logo = logo_path
            QtWidgets.QMessageBox.information(
                self,
                "Logo importé",
                f"Logo importé : {os.path.basename(logo_path)}\n\n"
                "Le logo sera utilisé après redémarrage de l'application."
            )

    def preview_theme(self):
        """Applique le thème sélectionné pour prévisualisation."""
        if not self._current_qss:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucun thème",
                "Veuillez d'abord sélectionner un fichier de thème avec le bouton 'Choisir un thème'."
            )
            return
        
        try:
            # Appliquer le thème à la fenêtre principale
            app = QtWidgets.QApplication.instance()
            if app:
                load_theme(self._current_qss, app)
                
                # Sauvegarder le choix
                save_theme_choice(self._current_qss, self._current_logo or "")
                
                QtWidgets.QMessageBox.information(
                    self,
                    "Thème appliqué",
                    "Le thème a été appliqué avec succès.\n"
                    "Il sera utilisé automatiquement au prochain démarrage."
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'application du thème : {str(e)}"
            )