# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/database_selector_dialog.py
Rôle : Dialogue de sélection/création de base de données au démarrage.
Permet de lister les bases existantes, en ouvrir une, ou en créer une nouvelle.
"""

import os
import json
from PyQt5 import QtWidgets
from club_manager.ui.database_selector_dialog_ui import Ui_DatabaseSelectorDialog

class DatabaseSelectorDialog(QtWidgets.QDialog, Ui_DatabaseSelectorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selected_db_path = None
        
        # Connexions
        self.buttonOpenSelected.clicked.connect(self.open_selected)
        self.buttonBrowse.clicked.connect(self.browse_database)
        self.buttonCreateNew.clicked.connect(self.create_new)
        self.buttonBox.rejected.connect(self.reject)
        self.listExistingDatabases.itemDoubleClicked.connect(self.open_selected)
        
        # Charger les bases existantes
        self.load_existing_databases()
        
        # Charger la dernière base utilisée
        self.load_last_database()
    
    def get_app_data_dir(self):
        """Retourne le répertoire de données de l'application."""
        home = os.path.expanduser("~")
        app_dir = os.path.join(home, ".clubmanager")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        return app_dir
    
    def get_config_file(self):
        """Retourne le chemin du fichier de configuration."""
        return os.path.join(self.get_app_data_dir(), "config.json")
    
    def load_last_database(self):
        """Charge le chemin de la dernière base utilisée."""
        config_file = self.get_config_file()
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    last_db = config.get('last_database')
                    if last_db and os.path.exists(last_db):
                        # Sélectionner cette base dans la liste
                        for i in range(self.listExistingDatabases.count()):
                            item = self.listExistingDatabases.item(i)
                            if item.data(QtWidgets.QListWidgetItem.UserType) == last_db:
                                self.listExistingDatabases.setCurrentItem(item)
                                break
            except:
                pass
    
    def save_last_database(self, db_path):
        """Sauvegarde le chemin de la dernière base utilisée."""
        config_file = self.get_config_file()
        config = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except:
                pass
        config['last_database'] = db_path
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_existing_databases(self):
        """Charge la liste des bases de données existantes."""
        app_dir = self.get_app_data_dir()
        self.listExistingDatabases.clear()
        
        # Chercher les fichiers .db dans le répertoire de l'application
        if os.path.exists(app_dir):
            for filename in os.listdir(app_dir):
                if filename.endswith('.db'):
                    db_path = os.path.join(app_dir, filename)
                    item = QtWidgets.QListWidgetItem(filename)
                    item.setData(QtWidgets.QListWidgetItem.UserType, db_path)
                    self.listExistingDatabases.addItem(item)
        
        # Aussi chercher dans le répertoire courant (pour compatibilité)
        current_dir = os.getcwd()
        for filename in os.listdir(current_dir):
            if filename.endswith('.db'):
                db_path = os.path.join(current_dir, filename)
                # Éviter les doublons
                already_added = False
                for i in range(self.listExistingDatabases.count()):
                    if self.listExistingDatabases.item(i).data(QtWidgets.QListWidgetItem.UserType) == db_path:
                        already_added = True
                        break
                if not already_added:
                    item = QtWidgets.QListWidgetItem(f"{filename} (répertoire courant)")
                    item.setData(QtWidgets.QListWidgetItem.UserType, db_path)
                    self.listExistingDatabases.addItem(item)
    
    def open_selected(self):
        """Ouvre la base de données sélectionnée."""
        current_item = self.listExistingDatabases.currentItem()
        if current_item:
            self.selected_db_path = current_item.data(QtWidgets.QListWidgetItem.UserType)
            self.save_last_database(self.selected_db_path)
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner une base de données dans la liste."
            )
    
    def browse_database(self):
        """Permet de parcourir pour sélectionner un fichier de base de données."""
        db_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Sélectionner une base de données",
            self.get_app_data_dir(),
            "Base de données (*.db);;Tous les fichiers (*.*)"
        )
        if db_path:
            self.selected_db_path = db_path
            self.save_last_database(self.selected_db_path)
            self.accept()
    
    def create_new(self):
        """Crée une nouvelle base de données."""
        db_name = self.editNewDbName.text().strip()
        if not db_name:
            QtWidgets.QMessageBox.warning(
                self,
                "Nom requis",
                "Veuillez saisir un nom pour la nouvelle base de données."
            )
            return
        
        # Ajouter l'extension .db si nécessaire
        if not db_name.endswith('.db'):
            db_name += '.db'
        
        # Créer dans le répertoire de l'application
        app_dir = self.get_app_data_dir()
        db_path = os.path.join(app_dir, db_name)
        
        # Vérifier si le fichier existe déjà
        if os.path.exists(db_path):
            reply = QtWidgets.QMessageBox.question(
                self,
                "Fichier existant",
                f"Le fichier {db_name} existe déjà. Voulez-vous l'ouvrir ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.selected_db_path = db_path
                self.save_last_database(self.selected_db_path)
                self.accept()
            return
        
        # Créer un fichier vide (sera initialisé par Database)
        self.selected_db_path = db_path
        self.save_last_database(self.selected_db_path)
        self.accept()
    
    def get_selected_database_path(self):
        """Retourne le chemin de la base de données sélectionnée."""
        return self.selected_db_path
