# -*- coding: utf-8 -*-
"""
Module d'export (CSV, PDF) des données Club Manager.
Utilise pandas pour CSV, ReportLab pour PDF.
"""

import csv
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pandas as pd
from club_manager.core.mjc_clubs import get_all_mjc_clubs

# Dictionnaire de traduction des champs en français
FIELD_TRANSLATIONS = {
    # Champs membres
    'id': 'ID',
    'last_name': 'Nom',
    'first_name': 'Prénom',
    'address': 'Adresse',
    'postal_code': 'Code postal',
    'city': 'Ville',
    'phone': 'Téléphone',
    'mail': 'Email',
    'rgpd': 'Consentement RGPD',
    'image_rights': 'Droit à l\'image',
    'payment_type': 'Type de paiement',
    'ancv_amount': 'Montant ANCV',
    'cash_amount': 'Montant espèces',
    'check1_amount': 'Montant chèque 1',
    'check2_amount': 'Montant chèque 2',
    'check3_amount': 'Montant chèque 3',
    'total_paid': 'Total payé',
    'mjc_club_id': 'Club MJC principal',
    'cotisation_status': 'Statut cotisation',
    'birth_date': 'Date de naissance',
    'other_mjc_clubs': 'Autres clubs MJC',
    # Champs postes
    'name': 'Nom',
    'type': 'Type',
    'description': 'Description',
    'assigned_to': 'Assigné à',
    # Champs clubs MJC
    'created_date': 'Date de création',
    # Champs prix annuels
    'year': 'Année',
    'club_price': 'Prix club',
    'mjc_price': 'Prix MJC',
    'is_current': 'En cours',
    # Champs cotisations
    'member_id': 'ID membre',
    'session_id': 'ID session',
    'amount': 'Montant',
    'paid': 'Payé',
    'payment_date': 'Date de paiement',
    'method': 'Méthode',
    'status': 'Statut',
    'cheque_number': 'Numéro de chèque',
}

def get_french_field_name(field_name):
    """
    Retourne le nom français d'un champ, ou une version formatée si non traduit.
    
    Args:
        field_name: Nom du champ en anglais
        
    Returns:
        Nom du champ en français
    """
    return FIELD_TRANSLATIONS.get(field_name, field_name.replace('_', ' ').title())

def resolve_mjc_club_names(data):
    """
    Résout les IDs de clubs MJC en noms de clubs dans les données.
    
    Args:
        data: Liste de dictionnaires contenant les données
        
    Returns:
        Liste de dictionnaires avec les IDs de clubs remplacés par les noms
    """
    # Créer un dictionnaire ID -> Nom pour une recherche rapide
    mjc_clubs = get_all_mjc_clubs()
    club_map = {club['id']: club['name'] for club in mjc_clubs}
    
    # Copier les données pour ne pas modifier l'original
    resolved_data = []
    for item in data:
        item_copy = dict(item)
        
        # Résoudre mjc_club_id
        if 'mjc_club_id' in item_copy and item_copy['mjc_club_id']:
            club_id = item_copy['mjc_club_id']
            item_copy['mjc_club_id'] = club_map.get(club_id, str(club_id))
        
        # Résoudre other_mjc_clubs (liste d'IDs au format JSON ou séparés par des virgules)
        if 'other_mjc_clubs' in item_copy and item_copy['other_mjc_clubs']:
            try:
                value = item_copy['other_mjc_clubs']
                club_ids = []
                
                # Essayer de parser comme JSON array d'abord (format: "[5]" ou "[5,3]")
                try:
                    parsed = json.loads(value) if isinstance(value, str) else value
                    if isinstance(parsed, list):
                        club_ids = parsed
                    else:
                        club_ids = [parsed]
                except (json.JSONDecodeError, TypeError):
                    # Si ce n'est pas du JSON, essayer de séparer par virgule
                    parts = str(value).split(',')
                    for part in parts:
                        try:
                            club_ids.append(int(part.strip()))
                        except ValueError:
                            # Ignorer les valeurs invalides plutôt que d'échouer
                            pass
                
                # Convertir en liste d'entiers de manière défensive
                valid_club_ids = []
                for id_val in club_ids:
                    try:
                        if isinstance(id_val, int):
                            valid_club_ids.append(id_val)
                        elif isinstance(id_val, str) and id_val.strip().isdigit():
                            valid_club_ids.append(int(id_val.strip()))
                        # Autres types ou valeurs invalides sont ignorés
                    except (ValueError, TypeError):
                        # Ignorer les IDs invalides plutôt que d'échouer
                        pass
                
                # Résoudre les IDs en noms de clubs
                if valid_club_ids:
                    club_names = [club_map.get(club_id, str(club_id)) for club_id in valid_club_ids]
                    item_copy['other_mjc_clubs'] = ', '.join(club_names)
            except AttributeError:
                # Si on ne peut pas parser (par exemple, item_copy n'est pas un dict), garder la valeur originale
                pass
        
        resolved_data.append(item_copy)
    
    return resolved_data

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
        from reportlab.lib.pagesizes import letter, A4, landscape
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
        # Convert sqlite3.Row objects to dictionaries for proper field access
        # The 'field in item' check (line 136) doesn't work with sqlite3.Row objects
        if data and not isinstance(data[0], dict):
            data = [dict(row) for row in data]
        
        # Résoudre les IDs de clubs MJC en noms de clubs
        data = resolve_mjc_club_names(data)
        
        # Déterminer les champs à afficher
        if selected_fields:
            fields = selected_fields
        else:
            fields = list(data[0].keys())
        
        # Déterminer l'orientation en fonction du nombre de colonnes
        # Portrait pour moins de 6 colonnes, paysage pour 6 colonnes ou plus
        num_cols = len(fields)
        if num_cols < 6:
            pagesize = A4
            orientation_text = "portrait"
        else:
            pagesize = landscape(A4)
            orientation_text = "paysage"
        
        # Créer le document PDF avec des marges réduites pour maximiser l'espace
        doc = SimpleDocTemplate(fname, pagesize=pagesize, 
                               leftMargin=0.3*inch, rightMargin=0.3*inch,
                               topMargin=0.3*inch, bottomMargin=0.3*inch)
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
        date_text = Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - Format: {orientation_text}", date_style)
        story.append(date_text)
        story.append(Spacer(1, 20))
        
        # Créer les en-têtes de table avec traduction française
        headers = [get_french_field_name(field) for field in fields]
        
        # Créer les données de la table avec retour à la ligne automatique
        table_data = [headers]
        for item in data:
            row = []
            for field in fields:
                value = item[field] if field in item else ''
                # Formater les valeurs booléennes
                if isinstance(value, bool):
                    value = 'Oui' if value else 'Non'
                elif isinstance(value, (int, float)) and field in ['rgpd', 'image_rights', 'rgpd_consent', 'image_consent']:
                    value = 'Oui' if value else 'Non'
                elif value is None:
                    value = ''
                
                # Convertir en Paragraph pour permettre le retour à la ligne
                cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=8, leading=10)
                cell_text = Paragraph(str(value), cell_style)
                row.append(cell_text)
            table_data.append(row)
        
        # Calculer les largeurs de colonnes de manière intelligente
        # Largeur disponible selon l'orientation (A4 = 8.27 x 11.69 inches)
        # Avec marges réduites de 0.3 inch de chaque côté
        if pagesize == A4:
            available_width = 7.67 * inch  # Portrait (8.27 - 0.6)
        else:
            available_width = 11.09 * inch  # Paysage (11.69 - 0.6)
        
        # Distribution intelligente de la largeur selon le type de colonne
        col_widths = []
        for field in fields:
            # Colonnes courtes (ID, booléens, statuts)
            if field in ['id', 'rgpd', 'image_rights', 'is_current']:
                col_widths.append(0.5 * inch)
            # Colonnes moyennes (noms, dates, montants)
            elif field in ['last_name', 'first_name', 'name', 'year', 'type', 'cotisation_status', 
                          'payment_type', 'birth_date', 'created_date', 'mjc_club_id']:
                col_widths.append(1.0 * inch)
            # Colonnes larges (adresses, descriptions, emails, clubs multiples)
            elif field in ['address', 'description', 'mail', 'details', 'other_mjc_clubs']:
                col_widths.append(1.5 * inch)
            # Par défaut
            else:
                col_widths.append(0.8 * inch)
        
        # Ajuster proportionnellement si la somme dépasse la largeur disponible
        total_width = sum(col_widths)
        if total_width > available_width:
            col_widths = [w * available_width / total_width for w in col_widths]
        
        # Créer la table
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Style de la table avec retour à la ligne
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Corps
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 1), (-1, -1), 4),
            ('RIGHTPADDING', (0, 1), (-1, -1), 4),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternance de couleurs pour les lignes
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            
            # Retour à la ligne automatique
            ('WORDWRAP', (0, 0), (-1, -1), True),
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
            f"Export PDF réussi :\n{fname}\n\n{len(data)} élément(s) exporté(s) en format {orientation_text}."
        )
        return True
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        QMessageBox.critical(parent, "Erreur d'export PDF", f"Erreur lors de l'export : {str(e)}\n\nDétails:\n{error_details}")
        return False