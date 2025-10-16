# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/sessions_tab.ui
Classe : Ui_SessionsTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_SessionsTab(object):
    def setupUi(self, SessionsTab):
        SessionsTab.setObjectName("SessionsTab")
        SessionsTab.resize(700, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(SessionsTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonAddSession = QtWidgets.QPushButton(SessionsTab)
        self.buttonAddSession.setText("Ajouter")
        self.buttonEditSession = QtWidgets.QPushButton(SessionsTab)
        self.buttonEditSession.setText("Modifier")
        self.buttonDeleteSession = QtWidgets.QPushButton(SessionsTab)
        self.buttonDeleteSession.setText("Supprimer")
        self.buttonExportSessions = QtWidgets.QPushButton(SessionsTab)
        self.buttonExportSessions.setText("Exporter")
        self.horizontalLayoutTop.addWidget(self.buttonAddSession)
        self.horizontalLayoutTop.addWidget(self.buttonEditSession)
        self.horizontalLayoutTop.addWidget(self.buttonDeleteSession)
        self.horizontalLayoutTop.addWidget(self.buttonExportSessions)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tableSessions = QtWidgets.QTableWidget(SessionsTab)
        self.tableSessions.setColumnCount(4)
        self.tableSessions.setHorizontalHeaderLabels([
            "Nom", "Début", "Fin", "Courante"
        ])
        self.verticalLayout.addWidget(self.tableSessions)
        self.buttonSetCurrent = QtWidgets.QPushButton(SessionsTab)
        self.buttonSetCurrent.setText("Définir comme session courante")
        self.verticalLayout.addWidget(self.buttonSetCurrent)