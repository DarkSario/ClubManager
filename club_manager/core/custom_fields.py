# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des champs personnalisés dans Club Manager.
Permet d'ajouter, modifier, supprimer et interroger les champs personnalisés définis par l'utilisateur.
"""

from .database import Database

def get_all_custom_fields():
    db = Database.instance()
    return db.query("SELECT * FROM custom_fields")

def add_custom_field(name, ftype, default_value, options, constraints):
    db = Database.instance()
    db.execute(
        "INSERT INTO custom_fields (name, type, default_value, options, constraints) VALUES (?, ?, ?, ?, ?)",
        (name, ftype, default_value, options, constraints)
    )

def update_custom_field(field_id, name, ftype, default_value, options, constraints):
    db = Database.instance()
    db.execute(
        "UPDATE custom_fields SET name=?, type=?, default_value=?, options=?, constraints=? WHERE id=?",
        (name, ftype, default_value, options, constraints, field_id)
    )

def delete_custom_field(field_id):
    db = Database.instance()
    db.execute("DELETE FROM custom_fields WHERE id=?", (field_id,))