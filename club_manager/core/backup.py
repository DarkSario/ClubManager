# -*- coding: utf-8 -*-
"""
Module de sauvegarde et restauration de la base (fichier .db) et des ressources.
"""
import shutil
import os
import zipfile
import tempfile
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt

def backup_database(db_path, parent=None):
    fname, _ = QFileDialog.getSaveFileName(parent, "Exporter la sauvegarde", "", "Fichier ZIP (*.zip)")
    if not fname:
        return
    try:
        shutil.make_archive(fname.replace(".zip", ""), 'zip', os.path.dirname(db_path))
        QMessageBox.information(parent, "Sauvegarde", "Sauvegarde réalisée avec succès.")
    except Exception as e:
        QMessageBox.critical(parent, "Erreur sauvegarde", str(e))

def restore_database(parent=None):
    fname, _ = QFileDialog.getOpenFileName(parent, "Restaurer une sauvegarde", "", "Fichier ZIP (*.zip)")
    if not fname:
        return
    try:
        shutil.unpack_archive(fname, os.path.dirname(fname), 'zip')
        QMessageBox.information(parent, "Restauration", "Restauration effectuée avec succès.\nRedémarrez l'application.")
    except Exception as e:
        QMessageBox.critical(parent, "Erreur restauration", str(e))

def export_zip_archive(parent=None):
    """Exporte la base de données actuelle avec toutes les ressources dans une archive ZIP."""
    from club_manager.core.database import Database
    
    # Demander le chemin de sauvegarde
    fname, _ = QFileDialog.getSaveFileName(
        parent, 
        "Exporter l'archive complète", 
        os.path.expanduser("~/clubmanager_export.zip"),
        "Fichier ZIP (*.zip)"
    )
    
    if not fname:
        return
    
    # S'assurer que le fichier a l'extension .zip
    if not fname.endswith('.zip'):
        fname += '.zip'
    
    try:
        # Créer une barre de progression
        progress = QProgressDialog("Export en cours...", "Annuler", 0, 100, parent)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(10)
        
        # Obtenir le chemin de la base de données actuelle
        db_path = Database.get_current_db_path()
        if not db_path or not os.path.exists(db_path):
            QMessageBox.warning(parent, "Erreur", "Aucune base de données active trouvée.")
            return
        
        progress.setValue(20)
        
        # Créer l'archive ZIP
        with zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le fichier de base de données
            zipf.write(db_path, os.path.basename(db_path))
            progress.setValue(60)
            
            # Ajouter les fichiers de configuration s'ils existent
            config_dir = os.path.expanduser('~/.clubmanager')
            if os.path.exists(config_dir):
                config_file = os.path.join(config_dir, 'config.json')
                if os.path.exists(config_file):
                    zipf.write(config_file, 'config.json')
            
            progress.setValue(90)
        
        progress.setValue(100)
        QMessageBox.information(
            parent, 
            "Export réussi", 
            f"L'archive a été créée avec succès :\n{fname}"
        )
    except Exception as e:
        QMessageBox.critical(parent, "Erreur d'export", f"Erreur lors de l'export : {str(e)}")

def import_zip_archive(parent=None):
    """Importe une archive ZIP contenant une base de données ClubManager."""
    from club_manager.core.database import Database
    
    # Demander le fichier à importer
    fname, _ = QFileDialog.getOpenFileName(
        parent, 
        "Importer une archive", 
        "",
        "Fichier ZIP (*.zip)"
    )
    
    if not fname:
        return
    
    try:
        # Créer une barre de progression
        progress = QProgressDialog("Import en cours...", "Annuler", 0, 100, parent)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(10)
        
        # Créer un répertoire temporaire pour extraire l'archive
        with tempfile.TemporaryDirectory() as temp_dir:
            progress.setValue(20)
            
            # Extraire l'archive
            with zipfile.ZipFile(fname, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            progress.setValue(50)
            
            # Trouver le fichier .db dans l'archive
            db_files = [f for f in os.listdir(temp_dir) if f.endswith('.db')]
            
            if not db_files:
                QMessageBox.warning(
                    parent, 
                    "Erreur", 
                    "Aucun fichier de base de données (.db) trouvé dans l'archive."
                )
                return
            
            # Prendre le premier fichier .db trouvé
            db_file = db_files[0]
            extracted_db_path = os.path.join(temp_dir, db_file)
            
            progress.setValue(70)
            
            # Demander où sauvegarder la base importée
            save_path, _ = QFileDialog.getSaveFileName(
                parent,
                "Enregistrer la base importée",
                os.path.expanduser(f"~/.clubmanager/{db_file}"),
                "Fichier de base de données (*.db)"
            )
            
            if not save_path:
                return
            
            # S'assurer que le fichier a l'extension .db
            if not save_path.endswith('.db'):
                save_path += '.db'
            
            # Créer le répertoire parent si nécessaire
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            progress.setValue(80)
            
            # Copier la base de données extraite vers l'emplacement choisi
            shutil.copy2(extracted_db_path, save_path)
            
            # Restaurer le fichier de config s'il existe dans l'archive
            config_file = os.path.join(temp_dir, 'config.json')
            if os.path.exists(config_file):
                config_dir = os.path.expanduser('~/.clubmanager')
                os.makedirs(config_dir, exist_ok=True)
                # Ne pas écraser le config actuel, seulement si confirmé
                reply = QMessageBox.question(
                    parent,
                    "Restaurer la configuration ?",
                    "L'archive contient un fichier de configuration. Voulez-vous le restaurer ?\n"
                    "(Cela écrasera votre configuration actuelle)",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    shutil.copy2(config_file, os.path.join(config_dir, 'config.json'))
            
            progress.setValue(100)
        
        QMessageBox.information(
            parent,
            "Import réussi",
            f"La base de données a été importée avec succès :\n{save_path}\n\n"
            f"Vous pouvez maintenant l'ouvrir via 'Fichier → Changer de base de données'."
        )
        
    except Exception as e:
        QMessageBox.critical(parent, "Erreur d'import", f"Erreur lors de l'import : {str(e)}")