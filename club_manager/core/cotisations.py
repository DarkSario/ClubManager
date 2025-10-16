# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des cotisations (paiements) dans Club Manager.
Permet d'ajouter, modifier, supprimer, lister les cotisations, relancer les membres.
"""

from .database import Database

def get_all_cotisations():
    db = Database.instance()
    return db.query("SELECT * FROM cotisations")

def add_cotisation(member_id, session_id, amount, paid, payment_date, method, status, cheque_number=None):
    db = Database.instance()
    db.execute(
        "INSERT INTO cotisations (member_id, session_id, amount, paid, payment_date, method, status, cheque_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (member_id, session_id, float(amount), float(paid), payment_date, method, status, cheque_number)
    )

def update_cotisation(cotisation_id, member_id, session_id, amount, paid, payment_date, method, status, cheque_number=None):
    db = Database.instance()
    db.execute(
        "UPDATE cotisations SET member_id=?, session_id=?, amount=?, paid=?, payment_date=?, method=?, status=?, cheque_number=? WHERE id=?",
        (member_id, session_id, float(amount), float(paid), payment_date, method, status, cheque_number, cotisation_id)
    )

def delete_cotisation(cotisation_id):
    db = Database.instance()
    db.execute("DELETE FROM cotisations WHERE id=?", (cotisation_id,))

def get_late_members():
    db = Database.instance()
    # Retourne les membres dont la cotisation n'est pas "Payé"
    return db.query("""
        SELECT m.*
        FROM members m
        JOIN cotisations c ON c.member_id = m.id
        WHERE c.status != 'Payé'
    """)