# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des prix annuels dans Club Manager.
Permet de gérer les prix Club et MJC pour chaque année.
"""

from .database import Database

def get_all_annual_prices():
    """Récupère tous les prix annuels."""
    db = Database.instance()
    return db.query("SELECT * FROM annual_prices ORDER BY year DESC")

def get_current_annual_price():
    """Récupère le prix annuel actuel."""
    db = Database.instance()
    rows = db.query("SELECT * FROM annual_prices WHERE is_current=1")
    return rows[0] if rows else None

def get_annual_price_by_year(year):
    """Récupère le prix annuel pour une année donnée."""
    db = Database.instance()
    rows = db.query("SELECT * FROM annual_prices WHERE year=?", (year,))
    return rows[0] if rows else None

def add_annual_price(year, club_price, mjc_price, is_current=False):
    """Ajoute un nouveau prix annuel."""
    db = Database.instance()
    if is_current:
        # Désactiver tous les autres prix courants
        db.execute("UPDATE annual_prices SET is_current=0")
    db.execute(
        "INSERT INTO annual_prices (year, club_price, mjc_price, is_current) VALUES (?, ?, ?, ?)",
        (year, float(club_price), float(mjc_price), int(is_current))
    )

def update_annual_price(price_id, year, club_price, mjc_price, is_current):
    """Met à jour un prix annuel."""
    db = Database.instance()
    if is_current:
        # Désactiver tous les autres prix courants
        db.execute("UPDATE annual_prices SET is_current=0")
    db.execute(
        "UPDATE annual_prices SET year=?, club_price=?, mjc_price=?, is_current=? WHERE id=?",
        (year, float(club_price), float(mjc_price), int(is_current), price_id)
    )

def delete_annual_price(price_id):
    """Supprime un prix annuel."""
    db = Database.instance()
    db.execute("DELETE FROM annual_prices WHERE id=?", (price_id,))

def set_current_annual_price(price_id):
    """Définit un prix annuel comme courant."""
    db = Database.instance()
    db.execute("UPDATE annual_prices SET is_current=0")
    db.execute("UPDATE annual_prices SET is_current=1 WHERE id=?", (price_id,))
