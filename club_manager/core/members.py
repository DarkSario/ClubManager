# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des membres (adhérents) dans Club Manager.
Permet d'ajouter, modifier, supprimer, rechercher les membres.
"""

import sqlite3
from typing import Any, Dict, List, Optional

from club_manager.core.database import Database
from club_manager.core.logger import get_logger

logger = get_logger(__name__)

# Colonnes autorisées dans les requêtes dynamiques (protection contre l'injection SQL)
MEMBER_COLUMNS = {
    "last_name",
    "first_name",
    "address",
    "postal_code",
    "city",
    "phone",
    "mail",
    "rgpd",
    "image_rights",
    "payment_type",
    "ancv_amount",
    "cash_amount",
    "check1_amount",
    "check2_amount",
    "check3_amount",
    "total_paid",
    "mjc_club_id",
    "cotisation_status",
    "birth_date",
    "other_mjc_clubs",
}

# Clés autorisées pour get_filtered_members
TEXT_FILTERS = ("last_name", "first_name", "city", "mail")
EXACT_FILTERS = ("cotisation_status", "payment_type")
BOOLEAN_FILTERS = ("rgpd", "image_rights")
ALLOWED_FILTERS = frozenset(TEXT_FILTERS + EXACT_FILTERS + BOOLEAN_FILTERS)


def _check_columns(fields: Dict[str, Any]) -> None:
    unknown = set(fields) - MEMBER_COLUMNS
    if unknown:
        raise ValueError(f"Champs inconnus: {', '.join(sorted(unknown))}")


def get_all_members() -> List[sqlite3.Row]:
    """Retourne tous les membres."""
    db = Database.instance()
    return db.query("SELECT * FROM members")


def get_member_by_id(member_id: int) -> Optional[sqlite3.Row]:
    """Retourne le membre d'identifiant ``member_id`` ou None."""
    db = Database.instance()
    rows = db.query("SELECT * FROM members WHERE id=?", (member_id,))
    return rows[0] if rows else None


def add_member(**fields: Any) -> None:
    """Ajoute un membre.

    Raises:
        ValueError: Si un champ n'est pas une colonne valide.
    """
    _check_columns(fields)
    db = Database.instance()
    keys = ",".join(fields)
    qmarks = ",".join(["?"] * len(fields))
    values = list(fields.values())
    sql = f"INSERT INTO members ({keys}) VALUES ({qmarks})"
    db.execute(sql, values)
    logger.info("Membre ajouté: %s %s", fields.get("last_name"), fields.get("first_name"))


def update_member(member_id: int, **fields: Any) -> None:
    """Met à jour un membre.

    Raises:
        ValueError: Si un champ n'est pas une colonne valide.
    """
    _check_columns(fields)
    db = Database.instance()
    set_clause = ",".join([f"{k}=?" for k in fields])
    values = list(fields.values()) + [member_id]
    sql = f"UPDATE members SET {set_clause} WHERE id=?"
    db.execute(sql, values)
    logger.info("Membre %s mis à jour", member_id)


def delete_member(member_id: int) -> None:
    """Supprime un membre."""
    db = Database.instance()
    db.execute("DELETE FROM members WHERE id=?", (member_id,))
    logger.info("Membre %s supprimé", member_id)


def get_filtered_members(filters: Optional[Dict[str, Any]]) -> List[sqlite3.Row]:
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

    Raises:
        ValueError: Si une clé de filtre n'est pas autorisée.
    """
    unknown = set(filters or {}) - ALLOWED_FILTERS
    if unknown:
        raise ValueError(
            f"Filtres inconnus: {', '.join(sorted(unknown))}. Filtres autorisés: {', '.join(sorted(ALLOWED_FILTERS))}"
        )
    if not filters:
        return get_all_members()

    db = Database.instance()

    # Construire la requête SQL dynamiquement
    where_clauses = []
    params = []

    # Filtres texte avec recherche partielle (LIKE)
    for field in TEXT_FILTERS:
        if field in filters:
            where_clauses.append(f"{field} LIKE ?")
            params.append(f"%{filters[field]}%")

    # Filtres exacts
    for field in EXACT_FILTERS + BOOLEAN_FILTERS:
        if field in filters:
            where_clauses.append(f"{field} = ?")
            params.append(filters[field])

    # Construire la requête finale
    sql = "SELECT * FROM members"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    return db.query(sql, params)
