# -*- coding: utf-8 -*-
"""
Module métier pour la gestion avancée des exports (sélection dynamique, preview, etc).
Complète `core/export.py` avec gestion dynamique des champs et prévisualisation.
"""

import csv
import pandas as pd
from club_manager.core.export import get_french_field_name, resolve_mjc_club_names

def preview_export(data, fields):
    """Retourne un DataFrame pandas avec seulement les champs demandés (pour preview dans QTableWidget)"""
    df = pd.DataFrame(data)
    return df[fields] if fields else df

def export_selected_csv(data, fields, fname):
    """Export CSV sur un sous-ensemble de champs."""
    df = pd.DataFrame(data)
    df[fields].to_csv(fname, index=False, encoding="utf-8")

def export_to_csv(data, file_path, delimiter=';', add_bom=False, selected_fields=None, translate_headers=True):
    """
    Exporte des données au format CSV avec gestion avancée du séparateur et du quoting.
    
    Args:
        data: Liste de dictionnaires ou d'objets sqlite3.Row contenant les données à exporter
        file_path: Chemin du fichier CSV de destination
        delimiter: Séparateur CSV (';', ',', ou '\\t'). Par défaut ';' pour la France
        add_bom: Si True, ajoute un BOM UTF-8 pour compatibilité Excel Windows
        selected_fields: Liste des champs à inclure (None = tous les champs)
        translate_headers: Si True, traduit les noms de colonnes en français
        
    Returns:
        Nombre de lignes exportées
        
    Raises:
        ValueError: Si les données sont vides ou invalides
    """
    if not data:
        raise ValueError("Aucune donnée à exporter")
    
    # Convertir les sqlite3.Row en dictionnaires si nécessaire
    if not isinstance(data[0], dict):
        data = [dict(row) for row in data]
    
    # Résoudre les IDs de clubs MJC en noms de clubs
    data = resolve_mjc_club_names(data)
    
    # Déterminer les champs à exporter
    if selected_fields:
        fields = selected_fields
    else:
        fields = list(data[0].keys())
    
    # Créer le mapping des en-têtes (nom technique -> nom français)
    if translate_headers:
        headers = [get_french_field_name(field) for field in fields]
    else:
        headers = fields
    
    # Mode d'ouverture du fichier
    mode = 'w'
    encoding = 'utf-8-sig' if add_bom else 'utf-8'
    
    # Exporter avec le module csv pour un meilleur contrôle
    with open(file_path, mode, newline='', encoding=encoding) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        
        # Écrire les en-têtes
        writer.writerow(headers)
        
        # Écrire les données
        for item in data:
            row = []
            for field in fields:
                value = item.get(field, '')
                
                # Formater les valeurs booléennes
                if isinstance(value, bool):
                    value = 'Oui' if value else 'Non'
                elif isinstance(value, (int, float)) and field in ['rgpd', 'image_rights', 'rgpd_consent', 'image_consent']:
                    value = 'Oui' if value else 'Non'
                elif value is None:
                    value = ''
                else:
                    value = str(value)
                
                row.append(value)
            
            writer.writerow(row)
    
    return len(data)