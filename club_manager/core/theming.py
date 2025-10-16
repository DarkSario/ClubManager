# -*- coding: utf-8 -*-
"""
Module métier pour la gestion de la thématisation (couleurs, logo, QSS) de Club Manager.
Gère le chargement, l'application et la sauvegarde des thèmes graphiques.
"""

import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def load_theme(qss_path, app):
    """Charge et applique un fichier QSS à l'application."""
    if not os.path.exists(qss_path):
        return
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

def import_logo(parent=None):
    """Importe un logo depuis le disque et retourne le chemin (à stocker)"""
    fname, _ = QFileDialog.getOpenFileName(parent, "Choisir un logo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
    return fname

def save_theme_choice(qss_path, logo_path, config_path="theme.conf"):
    """Sauvegarde le thème choisi (QSS et logo) dans un fichier de conf simple."""
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(f"qss={qss_path}\nlogo={logo_path}\n")

def load_theme_choice(config_path="theme.conf"):
    """Charge le thème choisi (QSS et logo) depuis le fichier de conf."""
    if not os.path.exists(config_path):
        return None, None
    qss = logo = None
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("qss="):
                qss = line[4:].strip()
            elif line.startswith("logo="):
                logo = line[5:].strip()
    return qss, logo