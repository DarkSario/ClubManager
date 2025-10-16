# -*- coding: utf-8 -*-
"""
Script de démarrage principal pour Club Manager.
Initialise l'application PyQt5, affiche la fenêtre principale.
"""

import sys
from PyQt5.QtWidgets import QApplication
from club_manager.main_window import MainWindow
from club_manager.ui.database_selector_dialog import DatabaseSelectorDialog

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Club Manager")
    app.setOrganizationName("DarkSario")
    app.setStyle("Fusion")
    
    # Afficher le dialogue de sélection de base de données
    db_selector = DatabaseSelectorDialog()
    if db_selector.exec_() != DatabaseSelectorDialog.Accepted:
        # L'utilisateur a annulé
        return 0
    
    db_path = db_selector.get_selected_database_path()
    if not db_path:
        return 0
    
    # Créer et afficher la fenêtre principale avec le chemin de la base
    window = MainWindow(db_path=db_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()