# -*- coding: utf-8 -*-
"""
Module métier pour la gestion avancée des exports (sélection dynamique, preview, etc).
Complète `core/export.py` avec gestion dynamique des champs et prévisualisation.
"""

import pandas as pd

def preview_export(data, fields):
    """Retourne un DataFrame pandas avec seulement les champs demandés (pour preview dans QTableWidget)"""
    df = pd.DataFrame(data)
    return df[fields] if fields else df

def export_selected_csv(data, fields, fname):
    """Export CSV sur un sous-ensemble de champs."""
    df = pd.DataFrame(data)
    df[fields].to_csv(fname, index=False, encoding="utf-8")