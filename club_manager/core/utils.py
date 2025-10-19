# -*- coding: utf-8 -*-
"""
Utilitaires transverses Club Manager (validation, génération, etc.)
"""

import re
import logging

logger = logging.getLogger(__name__)

def is_email_valid(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_phone_valid(phone):
    return bool(re.match(r"^0[1-9]([-. ]?\d{2}){4}$", phone))

def format_currency(amount):
    try:
        return "{:.2f} €".format(float(amount))
    except (ValueError, TypeError):
        return "0.00 €"

def safe_str(obj):
    try:
        return str(obj)
    except Exception:
        return ""

def safe_get_amount(member, key):
    """
    Récupère de manière sécurisée un montant depuis un membre.
    
    Args:
        member: Objet membre (dict-like)
        key: Clé du champ à récupérer
        
    Returns:
        float: Montant converti en float, 0.0 si null ou erreur
    """
    try:
        value = member.get(key) if hasattr(member, 'get') else member[key]
        return float(value) if value is not None else 0.0
    except (KeyError, ValueError, TypeError):
        return 0.0

def calculate_payment_totals(members):
    """
    Calcule les totaux des paiements à partir d'une liste de membres.
    
    Args:
        members: Liste de membres (dict-like objects avec cash_amount, check1_amount, 
                 check2_amount, check3_amount, ancv_amount)
    
    Returns:
        dict: Dictionnaire contenant:
            - 'total': Montant total global
            - 'cash': Montant total espèces
            - 'checks': Montant total chèques (somme check1 + check2 + check3)
            - 'ancv': Montant total ANCV
    """
    totals = {
        'total': 0.0,
        'cash': 0.0,
        'checks': 0.0,
        'ancv': 0.0
    }
    
    if not members:
        return totals
    
    for member in members:
        try:
            # Récupérer et additionner les montants
            totals['cash'] += safe_get_amount(member, 'cash_amount')
            
            check1 = safe_get_amount(member, 'check1_amount')
            check2 = safe_get_amount(member, 'check2_amount')
            check3 = safe_get_amount(member, 'check3_amount')
            totals['checks'] += check1 + check2 + check3
            
            totals['ancv'] += safe_get_amount(member, 'ancv_amount')
            
        except Exception as e:
            # Log l'erreur et continuer avec le membre suivant
            logger.warning(f"Erreur lors du calcul des totaux pour un membre : {e}")
            continue
    
    # Calculer le total global
    totals['total'] = totals['cash'] + totals['checks'] + totals['ancv']
    
    # Arrondir à 2 décimales
    for key in totals:
        totals[key] = round(totals[key], 2)
    
    return totals