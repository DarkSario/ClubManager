# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/exports_tab.py
Rôle : Onglet exports (ExportsTab) du Club Manager.
Hérite de QWidget et de Ui_ExportsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_ExportsTab généré par pyuic5 à partir de resources/ui/exports_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.exports_tab_ui import Ui_ExportsTab

class ExportsTab(QtWidgets.QWidget, Ui_ExportsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonExportCSV.clicked.connect(self.export_csv)
        self.buttonExportPDF.clicked.connect(self.export_pdf)
        self.buttonSelectFields.clicked.connect(self.select_fields)

    def export_csv(self):
        # Exporter les données en CSV
        pass

    def export_pdf(self):
        # Exporter les données en PDF
        pass

    def select_fields(self):
        # Ouvrir un dialog pour sélectionner les champs à exporter
        pass