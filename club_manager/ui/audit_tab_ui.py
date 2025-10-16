# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/audit_tab.ui
Classe : Ui_AuditTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_AuditTab(object):
    def setupUi(self, AuditTab):
        AuditTab.setObjectName("AuditTab")
        AuditTab.resize(900, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(AuditTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonExportAudit = QtWidgets.QPushButton(AuditTab)
        self.buttonExportAudit.setText("Exporter le journal")
        self.buttonPurgeRGPD = QtWidgets.QPushButton(AuditTab)
        self.buttonPurgeRGPD.setText("Purge RGPD")
        self.horizontalLayoutTop.addWidget(self.buttonExportAudit)
        self.horizontalLayoutTop.addWidget(self.buttonPurgeRGPD)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tableAudit = QtWidgets.QTableWidget(AuditTab)
        self.tableAudit.setColumnCount(5)
        self.tableAudit.setHorizontalHeaderLabels([
            "Date", "Action", "Utilisateur", "Objet", "Détail"
        ])
        self.verticalLayout.addWidget(self.tableAudit)