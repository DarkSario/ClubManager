# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des relances (cotisations en retard) dans Club Manager.
Gère la détection, la génération de relances et le suivi.
"""

from .database import Database

def get_members_to_remind():
    db = Database.instance()
    # Sélectionne les membres ayant au moins une cotisation non payée, par session
    return db.query("""
        SELECT m.*, s.name AS session_name, c.amount, c.paid, c.status
        FROM members m
        JOIN cotisations c ON c.member_id = m.id
        JOIN sessions s ON s.id = c.session_id
        WHERE c.status != 'Payé'
    """)

def mark_relance_sent(cotisation_id):
    db = Database.instance()
    db.execute("UPDATE cotisations SET status='Relancé' WHERE id=?", (cotisation_id,))