# -*- coding: utf-8 -*-
"""
Module d'export (CSV, PDF) des données Club Manager.
Utilise pandas pour CSV, ReportLab pour PDF.
"""

import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox
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

def export_to_pdf(data, data_type, selected_fields=None, parent=None):
    """
    Exporte des données au format PDF avec mise en page professionnelle.
    
    Args:
        data: Liste de dictionnaires contenant les données à exporter
        data_type: Type de données ('Membres', 'Postes', 'Clubs MJC', 'Prix annuels')
        selected_fields: Liste des champs à inclure (None = tous les champs)
        parent: Widget parent pour les dialogues
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        QMessageBox.warning(parent, "Erreur", "Le module reportlab n'est pas installé.\nInstallez-le avec: pip install reportlab")
        return False
    
    if not data:
        QMessageBox.information(parent, "Aucune donnée", f"Aucune donnée à exporter pour {data_type}.")
        return False
    
    # Demander le chemin de sauvegarde
    default_filename = f"{data_type.lower().replace(' ', '_')}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    fname, _ = QFileDialog.getSaveFileName(
        parent, 
        f"Exporter {data_type} en PDF", 
        os.path.expanduser(f"~/{default_filename}"),
        "Fichiers PDF (*.pdf)"
    )
    
    if not fname:
        return False
    
    try:
        # Créer le document PDF
        doc = SimpleDocTemplate(fname, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Titre
        title = Paragraph(f"Export {data_type}", title_style)
        story.append(title)
        
        # Date
        date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)
        date_text = Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", date_style)
        story.append(date_text)
        story.append(Spacer(1, 20))
        
        # Déterminer les champs à afficher
        if selected_fields:
            fields = selected_fields
        else:
            fields = list(data[0].keys())
        
        # Créer les en-têtes de table
        headers = [field.replace('_', ' ').title() for field in fields]
        
        # Créer les données de la table
        table_data = [headers]
        for item in data:
            row = []
            for field in fields:
                value = item.get(field, '')
                # Formater les valeurs booléennes
                if isinstance(value, bool):
                    value = 'Oui' if value else 'Non'
                elif isinstance(value, (int, float)) and field in ['rgpd_consent', 'image_consent']:
                    value = 'Oui' if value else 'Non'
                elif value is None:
                    value = ''
                row.append(str(value))
            table_data.append(row)
        
        # Calculer les largeurs de colonnes
        num_cols = len(fields)
        available_width = 7 * inch  # Largeur disponible sur A4 avec marges
        col_width = available_width / num_cols
        
        # Créer la table
        table = Table(table_data, colWidths=[col_width] * num_cols)
        
        # Style de la table
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Corps
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            
            # Alternance de couleurs pour les lignes
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(table)
        
        # Pied de page avec nombre total
        story.append(Spacer(1, 20))
        footer_text = Paragraph(f"<b>Total : {len(data)} élément(s)</b>", styles['Normal'])
        story.append(footer_text)
        
        # Générer le PDF
        doc.build(story)
        
        QMessageBox.information(
            parent,
            "Export réussi",
            f"Export PDF réussi :\n{fname}\n\n{len(data)} élément(s) exporté(s)."
        )
        return True
        
    except Exception as e:
        QMessageBox.critical(parent, "Erreur d'export PDF", f"Erreur lors de l'export : {str(e)}")
        return False