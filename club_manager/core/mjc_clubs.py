# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des clubs MJC dans Club Manager.
Permet d'ajouter, modifier, supprimer, lister les clubs MJC.
"""

from .database import Database
from datetime import datetime

def get_all_mjc_clubs():
    """Récupère tous les clubs MJC."""
    db = Database.instance()
    return db.query("SELECT * FROM mjc_clubs ORDER BY name")

def get_mjc_club_by_id(club_id):
    """Récupère un club MJC par son ID."""
    db = Database.instance()
    rows = db.query("SELECT * FROM mjc_clubs WHERE id=?", (club_id,))
    return rows[0] if rows else None

def add_mjc_club(name):
    """Ajoute un nouveau club MJC."""
    db = Database.instance()
    created_date = datetime.now().isoformat()
    db.execute(
        "INSERT INTO mjc_clubs (name, created_date) VALUES (?, ?)",
        (name, created_date)
    )

def update_mjc_club(club_id, name):
    """Met à jour un club MJC."""
    db = Database.instance()
    db.execute(
        "UPDATE mjc_clubs SET name=? WHERE id=?",
        (name, club_id)
    )

def delete_mjc_club(club_id):
    """Supprime un club MJC."""
    db = Database.instance()
    db.execute("DELETE FROM mjc_clubs WHERE id=?", (club_id,))
