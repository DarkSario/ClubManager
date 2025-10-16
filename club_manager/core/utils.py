# -*- coding: utf-8 -*-
"""
Utilitaires transverses Club Manager (validation, génération, etc.)
"""

import re

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