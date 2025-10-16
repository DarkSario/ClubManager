# -*- coding: utf-8 -*-
"""
Module d'export (CSV, PDF) des données Club Manager.
Utilise pandas pour CSV, ReportLab pour PDF.
"""

import csv
from PyQt5.QtWidgets import QFileDialog
import pandas as pd

def export_members_csv(members, parent=None):
    fname, _ = QFileDialog.getSaveFileName(parent, "Exporter en CSV", "", "Fichiers CSV (*.csv)")
    if not fname:
        return
    df = pd.DataFrame(members)
    df.to_csv(fname, index=False, encoding="utf-8")

def export_members_pdf(members, parent=None):
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(parent, "Erreur", "Le module reportlab n'est pas installé.")
        return
    fname, _ = QFileDialog.getSaveFileName(parent, "Exporter en PDF", "", "Fichiers PDF (*.pdf)")
    if not fname:
        return
    c = canvas.Canvas(fname)
    c.setFont("Helvetica", 10)
    y = 800
    for member in members:
        line = " | ".join(str(member[k]) for k in member.keys())
        c.drawString(40, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()