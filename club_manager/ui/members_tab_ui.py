# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/members_tab.ui
Classe : Ui_MembersTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_MembersTab(object):
    def setupUi(self, MembersTab):
        MembersTab.setObjectName("MembersTab")
        MembersTab.resize(900, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(MembersTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonAddMember = QtWidgets.QPushButton(MembersTab)
        self.buttonAddMember.setText("Ajouter")
        self.buttonEditMember = QtWidgets.QPushButton(MembersTab)
        self.buttonEditMember.setText("Modifier")
        self.buttonDeleteMember = QtWidgets.QPushButton(MembersTab)
        self.buttonDeleteMember.setText("Supprimer")
        self.buttonExportMembers = QtWidgets.QPushButton(MembersTab)
        self.buttonExportMembers.setText("Exporter")
        self.buttonMailing = QtWidgets.QPushButton(MembersTab)
        self.buttonMailing.setText("Mailing")
        self.horizontalLayoutTop.addWidget(self.buttonAddMember)
        self.horizontalLayoutTop.addWidget(self.buttonEditMember)
        self.horizontalLayoutTop.addWidget(self.buttonDeleteMember)
        self.horizontalLayoutTop.addWidget(self.buttonExportMembers)
        self.horizontalLayoutTop.addWidget(self.buttonMailing)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.tableMembers = QtWidgets.QTableWidget(MembersTab)
        self.tableMembers.setColumnCount(10)
        self.tableMembers.setHorizontalHeaderLabels([
            "Nom", "Prénom", "Adresse", "CP", "Ville", "Tél", "Mail", "RGPD", "Droit image", "Cotisation"
        ])
        self.verticalLayout.addWidget(self.tableMembers)
        self.horizontalLayoutFilter = QtWidgets.QHBoxLayout()
        self.buttonFilter = QtWidgets.QPushButton(MembersTab)
        self.buttonFilter.setText("Filtrer")
        self.buttonResetFilter = QtWidgets.QPushButton(MembersTab)
        self.buttonResetFilter.setText("Réinitialiser")
        self.horizontalLayoutFilter.addWidget(self.buttonFilter)
        self.horizontalLayoutFilter.addWidget(self.buttonResetFilter)
        self.verticalLayout.addLayout(self.horizontalLayoutFilter)