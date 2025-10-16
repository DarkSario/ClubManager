# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des postes (positions) dans Club Manager.
Permet d'ajouter, modifier, supprimer, lister les postes.
"""

from .database import Database

def get_all_positions():
    db = Database.instance()
    return db.query("SELECT * FROM positions")

def add_position(name, type, description, assigned_to=None):
    db = Database.instance()
    db.execute(
        "INSERT INTO positions (name, type, description, assigned_to) VALUES (?, ?, ?, ?)",
        (name, type, description, assigned_to)
    )

def update_position(position_id, name, type, description, assigned_to):
    db = Database.instance()
    db.execute(
        "UPDATE positions SET name=?, type=?, description=?, assigned_to=? WHERE id=?",
        (name, type, description, assigned_to, position_id)
    )

def delete_position(position_id):
    db = Database.instance()
    db.execute("DELETE FROM positions WHERE id=?", (position_id,))