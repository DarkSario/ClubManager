# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/positions_tab.ui
Classe : Ui_PositionsTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_PositionsTab(object):
    def setupUi(self, PositionsTab):
        PositionsTab.setObjectName("PositionsTab")
        PositionsTab.resize(700, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(PositionsTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonAddPosition = QtWidgets.QPushButton(PositionsTab)
        self.buttonAddPosition.setText("Ajouter")
        self.buttonEditPosition = QtWidgets.QPushButton(PositionsTab)
        self.buttonEditPosition.setText("Modifier")
        self.buttonDeletePosition = QtWidgets.QPushButton(PositionsTab)
        self.buttonDeletePosition.setText("Supprimer")
        self.buttonExportPositions = QtWidgets.QPushButton(PositionsTab)
        self.buttonExportPositions.setText("Exporter")
        self.horizontalLayoutTop.addWidget(self.buttonAddPosition)
        self.horizontalLayoutTop.addWidget(self.buttonEditPosition)
        self.horizontalLayoutTop.addWidget(self.buttonDeletePosition)
        self.horizontalLayoutTop.addWidget(self.buttonExportPositions)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tablePositions = QtWidgets.QTableWidget(PositionsTab)
        self.tablePositions.setColumnCount(3)
        self.tablePositions.setHorizontalHeaderLabels([
            "Poste", "Type", "Affecté à"
        ])
        self.verticalLayout.addWidget(self.tablePositions)
        self.horizontalLayoutBottom = QtWidgets.QHBoxLayout()
        self.buttonAffect = QtWidgets.QPushButton(PositionsTab)
        self.buttonAffect.setText("Affecter à un membre")
        self.buttonUnaffect = QtWidgets.QPushButton(PositionsTab)
        self.buttonUnaffect.setText("Désaffecter")
        self.horizontalLayoutBottom.addWidget(self.buttonAffect)
        self.horizontalLayoutBottom.addWidget(self.buttonUnaffect)
        self.verticalLayout.addLayout(self.horizontalLayoutBottom)