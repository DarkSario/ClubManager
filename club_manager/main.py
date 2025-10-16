# -*- coding: utf-8 -*-
"""
Script de démarrage principal pour Club Manager.
Initialise l'application PyQt5, affiche la fenêtre principale.
"""

import sys
from PyQt5.QtWidgets import QApplication
from club_manager.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Club Manager")
    app.setOrganizationName("DarkSario")
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()