# -*- coding: utf-8 -*-
"""
Module de journalisation des actions (audit) pour Club Manager.
Permet de tracer toutes les opérations sensibles.
"""

from datetime import datetime
from .database import Database

def log_action(action, user, obj, details):
    """Enregistre une action dans le journal d'audit."""
    db = Database.instance()
    db.execute(
        "INSERT INTO audit (date, action, user, object, details) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), action, user, obj, details)
    )

def get_all_audit_entries():
    """Récupère toutes les entrées d'audit."""
    db = Database.instance()
    return db.query("SELECT * FROM audit ORDER BY date DESC")

def delete_old_audit_entries(days=365):
    """Supprime les entrées d'audit plus anciennes que le nombre de jours spécifié."""
    db = Database.instance()
    cutoff_date = datetime.now().replace(year=datetime.now().year - (days // 365))
    db.execute("DELETE FROM audit WHERE date < ?", (cutoff_date.isoformat(),))