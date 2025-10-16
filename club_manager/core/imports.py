# -*- coding: utf-8 -*-
"""
Module métier pour l'import de données CSV (membres, cotisations, etc.) dans Club Manager.
Gère le mapping dynamique entre colonnes du CSV et champs internes.
"""

import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from .database import Database

def import_csv_to_table(table, field_map, parent=None):
    """Importe un CSV dans une table donnée via un mapping {col_csv: champ_table}."""
    fname, _ = QFileDialog.getOpenFileName(parent, "Importer un fichier CSV", "", "Fichiers CSV (*.csv)")
    if not fname:
        return
    db = Database.instance()
    with open(fname, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            values = [row.get(col, "") for col in field_map.keys()]
            placeholders = ','.join(['?'] * len(field_map))
            columns = ','.join(field_map.values())
            db.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
            count += 1
    QMessageBox.information(parent, "Import terminé", f"{count} lignes importées dans {table}.")

def guess_csv_fields(fname):
    """Retourne les noms de colonnes du CSV pour mapping dynamique."""
    with open(fname, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        return next(reader)