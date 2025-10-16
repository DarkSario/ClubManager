# -*- coding: utf-8 -*-
"""
Fichier UI pour le dialogue de sélection de base de données.
Classe : Ui_DatabaseSelectorDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_DatabaseSelectorDialog(object):
    def setupUi(self, DatabaseSelectorDialog):
        DatabaseSelectorDialog.setObjectName("DatabaseSelectorDialog")
        DatabaseSelectorDialog.resize(600, 400)
        DatabaseSelectorDialog.setWindowTitle("Sélection de la base de données")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(DatabaseSelectorDialog)
        
        # Titre
        self.labelTitle = QtWidgets.QLabel(DatabaseSelectorDialog)
        self.labelTitle.setText("<h2>Bienvenue dans Club Manager</h2>")
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelTitle)
        
        # Description
        self.labelDescription = QtWidgets.QLabel(DatabaseSelectorDialog)
        self.labelDescription.setText(
            "Sélectionnez une base de données existante ou créez-en une nouvelle.\n"
            "Chaque base de données correspond à une saison/année."
        )
        self.labelDescription.setWordWrap(True)
        self.labelDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labelDescription)
        
        # Groupe pour ouvrir une base existante
        self.groupExisting = QtWidgets.QGroupBox(DatabaseSelectorDialog)
        self.groupExisting.setTitle("Ouvrir une base existante")
        self.vLayoutExisting = QtWidgets.QVBoxLayout(self.groupExisting)
        
        self.listExistingDatabases = QtWidgets.QListWidget(self.groupExisting)
        self.vLayoutExisting.addWidget(self.listExistingDatabases)
        
        self.hLayoutExistingButtons = QtWidgets.QHBoxLayout()
        self.buttonOpenSelected = QtWidgets.QPushButton(self.groupExisting)
        self.buttonOpenSelected.setText("Ouvrir la base sélectionnée")
        self.buttonBrowse = QtWidgets.QPushButton(self.groupExisting)
        self.buttonBrowse.setText("Parcourir...")
        self.hLayoutExistingButtons.addWidget(self.buttonOpenSelected)
        self.hLayoutExistingButtons.addWidget(self.buttonBrowse)
        self.vLayoutExisting.addLayout(self.hLayoutExistingButtons)
        
        self.verticalLayout.addWidget(self.groupExisting)
        
        # Groupe pour créer une nouvelle base
        self.groupNew = QtWidgets.QGroupBox(DatabaseSelectorDialog)
        self.groupNew.setTitle("Créer une nouvelle base")
        self.vLayoutNew = QtWidgets.QVBoxLayout(self.groupNew)
        
        self.formLayout = QtWidgets.QFormLayout()
        self.editNewDbName = QtWidgets.QLineEdit(self.groupNew)
        self.editNewDbName.setPlaceholderText("Ex: ClubManager_2024-2025")
        self.formLayout.addRow("Nom de la base :", self.editNewDbName)
        self.vLayoutNew.addLayout(self.formLayout)
        
        self.buttonCreateNew = QtWidgets.QPushButton(self.groupNew)
        self.buttonCreateNew.setText("Créer une nouvelle base")
        self.vLayoutNew.addWidget(self.buttonCreateNew)
        
        self.verticalLayout.addWidget(self.groupNew)
        
        # Boutons standard
        self.buttonBox = QtWidgets.QDialogButtonBox(DatabaseSelectorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)
