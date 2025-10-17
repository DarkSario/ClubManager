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
    
    # Si c'est une nouvelle base, initialiser la base et afficher le dialogue des tarifs
    from club_manager.core.database import Database
    from club_manager.core.annual_prices import get_current_annual_price
    
    db = Database.instance(db_path)
    
    # Vérifier si des tarifs existent déjà
    current_price = get_current_annual_price()
    
    # Si c'est une nouvelle base ou qu'il n'y a pas de tarifs, afficher le dialogue
    if db_selector.is_new_database_created() or not current_price:
        from club_manager.ui.initial_prices_dialog import InitialPricesDialog
        prices_dialog = InitialPricesDialog()
        if prices_dialog.exec_() != InitialPricesDialog.Accepted:
            # L'utilisateur a annulé la configuration des tarifs
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                None,
                "Configuration incomplète",
                "La configuration des tarifs est obligatoire. L'application va se fermer."
            )
            return 0
    
    # Créer et afficher la fenêtre principale avec le chemin de la base
    window = MainWindow(db_path=db_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()