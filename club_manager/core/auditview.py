# -*- coding: utf-8 -*-
"""
Module métier pour la consultation/filtrage du journal d'audit.
Permet de lister, filtrer, exporter les entrées d'audit.
"""

from .database import Database

def get_all_audit_entries():
    db = Database.instance()
    return db.query("SELECT * FROM audit ORDER BY date DESC")

def get_audit_by_user(user):
    db = Database.instance()
    return db.query("SELECT * FROM audit WHERE user=? ORDER BY date DESC", (user,))

def get_audit_by_action(action):
    db = Database.instance()
    return db.query("SELECT * FROM audit WHERE action=? ORDER BY date DESC", (action,))

def delete_audit_entry(audit_id):
    db = Database.instance()
    db.execute("DELETE FROM audit WHERE id=?", (audit_id,))