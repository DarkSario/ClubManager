# -*- coding: utf-8 -*-
"""
Module métier RGPD pour Club Manager.
Gère la purge RGPD (anonymisation, suppression des données sensibles des anciens membres).
"""
from .database import Database

def purge_rgpd():
    db = Database.instance()
    # Exemple : anonymisation de tous les membres dont l’adhésion est expirée (>2 ans, ici simplifié)
    db.execute("""
        UPDATE members
        SET last_name='ANONYMISE', first_name='ANONYMISE', address='', postal_code='', city='',
            phone='', mail='', health='', external_club='', mjc_elsewhere=''
        WHERE id IN (
            SELECT m.id
            FROM members m
            LEFT JOIN cotisations c ON c.member_id = m.id
            WHERE c.payment_date IS NULL OR c.payment_date < date('now', '-2 years')
        )
    """)
    # Suppression en cascade des cotisations de ces membres si souhaité :
    # db.execute("DELETE FROM cotisations WHERE member_id IN (SELECT id FROM members WHERE last_name='ANONYMISE')")

def is_rgpd_ready(member):
    """Vérifie si le membre coche toutes les cases RGPD (consentement, etc.)"""
    return bool(member["rgpd"] if member["rgpd"] is not None else 0)