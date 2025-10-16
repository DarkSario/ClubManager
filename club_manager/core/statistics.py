# -*- coding: utf-8 -*-
"""
Module métier pour les statistiques et tableaux de bord de Club Manager.
Permet de calculer ratios, répartitions, historiques pour affichage graphique ou synthèse.
"""

from .database import Database

def count_members():
    db = Database.instance()
    rows = db.query("SELECT COUNT(*) AS count FROM members")
    return rows[0]["count"] if rows else 0

def count_members_by_city():
    db = Database.instance()
    return db.query("SELECT city, COUNT(*) AS count FROM members GROUP BY city ORDER BY count DESC")

def count_cotisations_by_status():
    db = Database.instance()
    return db.query("SELECT status, COUNT(*) AS count FROM cotisations GROUP BY status")

def total_collected_fees():
    db = Database.instance()
    rows = db.query("SELECT SUM(paid) AS total FROM cotisations")
    return rows[0]["total"] if rows else 0

def session_history():
    db = Database.instance()
    return db.query("""
        SELECT s.name, COUNT(c.id) AS nb_adhesions, SUM(c.paid) AS montant_total
        FROM sessions s
        LEFT JOIN cotisations c ON c.session_id = s.id
        GROUP BY s.name
        ORDER BY s.start DESC
    """)