# -*- coding: utf-8 -*-
"""
Module de sauvegarde et restauration de la base (fichier .db) et des ressources.
"""
import shutil
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

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

# Fonctions stub pour l'export/import ZIP complet (pour compatibilité UI)
def export_zip_archive(parent=None):
    QMessageBox.information(parent, "Export ZIP", "L'export ZIP complet n'est pas encore implémenté.")

def import_zip_archive(parent=None):
    QMessageBox.information(parent, "Import ZIP", "L'import ZIP complet n'est pas encore implémenté.")