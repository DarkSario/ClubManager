# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/cotisations_tab.ui
Classe : Ui_CotisationsTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_CotisationsTab(object):
    def setupUi(self, CotisationsTab):
        CotisationsTab.setObjectName("CotisationsTab")
        CotisationsTab.resize(800, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(CotisationsTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonAddCotisation = QtWidgets.QPushButton(CotisationsTab)
        self.buttonAddCotisation.setText("Ajouter")
        self.buttonEditCotisation = QtWidgets.QPushButton(CotisationsTab)
        self.buttonEditCotisation.setText("Modifier")
        self.buttonDeleteCotisation = QtWidgets.QPushButton(CotisationsTab)
        self.buttonDeleteCotisation.setText("Supprimer")
        self.buttonExportCotisations = QtWidgets.QPushButton(CotisationsTab)
        self.buttonExportCotisations.setText("Exporter")
        self.horizontalLayoutTop.addWidget(self.buttonAddCotisation)
        self.horizontalLayoutTop.addWidget(self.buttonEditCotisation)
        self.horizontalLayoutTop.addWidget(self.buttonDeleteCotisation)
        self.horizontalLayoutTop.addWidget(self.buttonExportCotisations)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tableCotisations = QtWidgets.QTableWidget(CotisationsTab)
        self.tableCotisations.setColumnCount(7)
        self.tableCotisations.setHorizontalHeaderLabels([
            "Membre", "Session", "Montant", "Payé", "Date", "Méthode", "Statut"
        ])
        self.verticalLayout.addWidget(self.tableCotisations)
        self.buttonRelance = QtWidgets.QPushButton(CotisationsTab)
        self.buttonRelance.setText("Relancer les adhérents en retard")
        self.verticalLayout.addWidget(self.buttonRelance)