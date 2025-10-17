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

def get_filtered_members(filters):
    """
    Récupère les membres selon les critères de filtrage.
    
    Args:
        filters (dict): Dictionnaire des filtres à appliquer
            - last_name: Nom (recherche partielle)
            - first_name: Prénom (recherche partielle)
            - city: Ville (recherche partielle)
            - mail: Email (recherche partielle)
            - cotisation_status: Statut exact de cotisation
            - payment_type: Type de paiement exact
            - rgpd: Consentement RGPD (0 ou 1)
            - image_rights: Droit à l'image (0 ou 1)
    
    Returns:
        list: Liste des membres correspondant aux critères
    """
    if not filters:
        return get_all_members()
    
    db = Database.instance()
    
    # Construire la requête SQL dynamiquement
    where_clauses = []
    params = []
    
    # Filtres texte avec recherche partielle (LIKE)
    text_filters = ['last_name', 'first_name', 'city', 'mail']
    for field in text_filters:
        if field in filters:
            where_clauses.append(f"{field} LIKE ?")
            params.append(f"%{filters[field]}%")
    
    # Filtres exacts
    exact_filters = ['cotisation_status', 'payment_type', 'rgpd', 'image_rights']
    for field in exact_filters:
        if field in filters:
            where_clauses.append(f"{field} = ?")
            params.append(filters[field])
    
    # Construire la requête finale
    sql = "SELECT * FROM members"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    
    return db.query(sql, params)