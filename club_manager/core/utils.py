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
    except Exception:
        return str(amount)

def safe_str(obj):
    try:
        return str(obj)
    except Exception:
        return ""

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
            # Récupérer et convertir les montants espèces
            cash_amount = member.get('cash_amount') if hasattr(member, 'get') else member['cash_amount']
            cash = float(cash_amount) if cash_amount is not None else 0.0
            totals['cash'] += cash
            
            # Récupérer et convertir les montants chèques
            check1 = member.get('check1_amount') if hasattr(member, 'get') else member['check1_amount']
            check1 = float(check1) if check1 is not None else 0.0
            
            check2 = member.get('check2_amount') if hasattr(member, 'get') else member['check2_amount']
            check2 = float(check2) if check2 is not None else 0.0
            
            check3 = member.get('check3_amount') if hasattr(member, 'get') else member['check3_amount']
            check3 = float(check3) if check3 is not None else 0.0
            
            checks_total = check1 + check2 + check3
            totals['checks'] += checks_total
            
            # Récupérer et convertir les montants ANCV
            ancv_amount = member.get('ancv_amount') if hasattr(member, 'get') else member['ancv_amount']
            ancv = float(ancv_amount) if ancv_amount is not None else 0.0
            totals['ancv'] += ancv
            
        except (KeyError, ValueError, TypeError) as e:
            # Log l'erreur et continuer avec le membre suivant
            logger.warning(f"Erreur lors du calcul des totaux pour un membre : {e}")
            continue
    
    # Calculer le total global
    totals['total'] = totals['cash'] + totals['checks'] + totals['ancv']
    
    # Arrondir à 2 décimales
    for key in totals:
        totals[key] = round(totals[key], 2)
    
    return totals