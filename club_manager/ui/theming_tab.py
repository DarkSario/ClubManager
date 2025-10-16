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

class ThemingTab(QtWidgets.QWidget, Ui_ThemingTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonChooseTheme.clicked.connect(self.choose_theme)
        self.buttonImportLogo.clicked.connect(self.import_logo)
        self.buttonPreviewTheme.clicked.connect(self.preview_theme)

    def choose_theme(self):
        # Choisir un thème graphique
        from club_manager.core.theming import save_theme_choice, load_theme
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un thème",
            "",
            "Fichiers QSS (*.qss);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                # Sauvegarder le choix
                save_theme_choice(file_path)
                
                # Appliquer le thème
                app = QtWidgets.QApplication.instance()
                load_theme(file_path, app)
                
                QtWidgets.QMessageBox.information(self, "Succès", f"Thème appliqué : {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'application du thème : {str(e)}")

    def import_logo(self):
        # Importer un logo
        from PyQt5.QtWidgets import QFileDialog
        import shutil
        import os
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer un logo",
            "",
            "Images (*.png *.jpg *.jpeg *.svg);;Tous les fichiers (*)"
        )
        
        if file_path:
            try:
                # Déterminer le répertoire de destination
                dest_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'images')
                os.makedirs(dest_dir, exist_ok=True)
                
                # Copier le fichier
                dest_path = os.path.join(dest_dir, 'custom_logo' + os.path.splitext(file_path)[1])
                shutil.copy(file_path, dest_path)
                
                QtWidgets.QMessageBox.information(
                    self,
                    "Succès",
                    f"Logo importé avec succès.\nEmplacement : {dest_path}"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'import du logo : {str(e)}")

    def preview_theme(self):
        # Prévisualiser le thème
        from club_manager.core.theming import load_theme_choice
        
        qss_path, _ = load_theme_choice()
        
        if qss_path:
            QtWidgets.QMessageBox.information(
                self,
                "Thème actuel",
                f"Thème actuellement appliqué :\n{qss_path}"
            )
        else:
            QtWidgets.QMessageBox.information(
                self,
                "Thème actuel",
                "Aucun thème personnalisé n'est appliqué.\nThème par défaut en cours d'utilisation."
            )