# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/exports_tab.ui
Classe : Ui_ExportsTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_ExportsTab(object):
    def setupUi(self, ExportsTab):
        ExportsTab.setObjectName("ExportsTab")
        ExportsTab.resize(700, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(ExportsTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonExportCSV = QtWidgets.QPushButton(ExportsTab)
        self.buttonExportCSV.setText("Exporter CSV")
        self.buttonExportPDF = QtWidgets.QPushButton(ExportsTab)
        self.buttonExportPDF.setText("Exporter PDF")
        self.buttonSelectFields = QtWidgets.QPushButton(ExportsTab)
        self.buttonSelectFields.setText("Champs à exporter")
        self.horizontalLayoutTop.addWidget(self.buttonExportCSV)
        self.horizontalLayoutTop.addWidget(self.buttonExportPDF)
        self.horizontalLayoutTop.addWidget(self.buttonSelectFields)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tablePreview = QtWidgets.QTableWidget(ExportsTab)
        self.tablePreview.setColumnCount(0)
        self.tablePreview.setRowCount(0)
        self.verticalLayout.addWidget(self.tablePreview)