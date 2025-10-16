# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des membres (adhérents) dans Club Manager.
Permet d'ajouter, modifier, supprimer, rechercher les membres.
"""

from .database import Database

def get_all_members():
    db = Database.instance()
    return db.query("SELECT * FROM members")

def get_member_by_id(member_id):
    db = Database.instance()
    rows = db.query("SELECT * FROM members WHERE id=?", (member_id,))
    return rows[0] if rows else None

def add_member(**fields):
    db = Database.instance()
    keys = ','.join(fields.keys())
    qmarks = ','.join(['?']*len(fields))
    values = list(fields.values())
    sql = f"INSERT INTO members ({keys}) VALUES ({qmarks})"
    db.execute(sql, values)

def update_member(member_id, **fields):
    db = Database.instance()
    set_clause = ','.join([f"{k}=?" for k in fields.keys()])
    values = list(fields.values()) + [member_id]
    sql = f"UPDATE members SET {set_clause} WHERE id=?"
    db.execute(sql, values)

def delete_member(member_id):
    db = Database.instance()
    db.execute("DELETE FROM members WHERE id=?", (member_id,))