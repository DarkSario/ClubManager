# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des sessions (saisons/périodes) dans Club Manager.
Permet d'ajouter, modifier, supprimer, lister les sessions, définir la session courante.
"""

from .database import Database

def get_all_sessions():
    db = Database.instance()
    return db.query("SELECT * FROM sessions")

def add_session(name, start, end, club_amount, mjc_amount, is_current=False):
    db = Database.instance()
    if is_current:
        db.execute("UPDATE sessions SET is_current=0")
    db.execute(
        "INSERT INTO sessions (name, start, end, club_amount, mjc_amount, is_current) VALUES (?, ?, ?, ?, ?, ?)",
        (name, start, end, club_amount, mjc_amount, int(is_current))
    )

def update_session(session_id, name, start, end, club_amount, mjc_amount, is_current):
    db = Database.instance()
    if is_current:
        db.execute("UPDATE sessions SET is_current=0")
    db.execute(
        "UPDATE sessions SET name=?, start=?, end=?, club_amount=?, mjc_amount=?, is_current=? WHERE id=?",
        (name, start, end, club_amount, mjc_amount, int(is_current), session_id)
    )

def delete_session(session_id):
    db = Database.instance()
    db.execute("DELETE FROM sessions WHERE id=?", (session_id,))

def set_current_session(session_id):
    db = Database.instance()
    db.execute("UPDATE sessions SET is_current=0")
    db.execute("UPDATE sessions SET is_current=1 WHERE id=?", (session_id,))