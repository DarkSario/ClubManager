# -*- coding: utf-8 -*-
"""
Module de journalisation des actions (audit) pour Club Manager.
Permet de tracer toutes les opérations sensibles.
"""

from datetime import datetime
from .database import Database

def log_action(action, user, obj, details):
    db = Database.instance()
    db.execute(
        "INSERT INTO audit (date, action, user, object, details) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), action, user, obj, details)
    )