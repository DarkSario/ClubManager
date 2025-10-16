# -*- coding: utf-8 -*-
"""
Module métier avancé pour le mailing de Club Manager.
Gère la sélection dynamique, la personnalisation de masse, les modèles (templates) et les pièces jointes.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyQt5.QtWidgets import QMessageBox, QFileDialog

def select_recipients(members, filters=None):
    """Filtre dynamiquement les membres selon des critères (ex: statut cotisation, session, etc.)."""
    if not filters:
        return members
    return [m for m in members if all(m.get(k) == v for k, v in filters.items())]

def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def personalize_template(template, context):
    """Remplace les variables du template par les valeurs du contexte (ex: {prenom}, {nom})"""
    for k, v in context.items():
        template = template.replace("{" + k + "}", str(v))
    return template

def select_attachments(parent=None):
    """Ouvre un sélecteur de fichiers pour pièces jointes, retourne la liste des chemins."""
    files, _ = QFileDialog.getOpenFileNames(parent, "Sélectionnez les pièces jointes")
    return files

def send_mass_mail(subject, template, members, smtp_config, parent=None, attachments=None):
    """Envoie un mailing personnalisé à chaque membre (remplacement tags, pièces jointes, etc.)."""
    errors = []
    for m in members:
        msg = MIMEMultipart()
        context = {k: m.get(k, "") for k in m.keys()}
        msg.attach(MIMEText(personalize_template(template, context), "plain", "utf-8"))
        msg["Subject"] = subject
        msg["From"] = smtp_config["from"]
        msg["To"] = m.get("mail", "")

        # Ajout pièces jointes
        if attachments:
            for fname in attachments:
                if os.path.isfile(fname):
                    with open(fname, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(fname))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(fname)}"'
                        msg.attach(part)

        try:
            with smtplib.SMTP(smtp_config["host"], smtp_config.get("port", 25)) as server:
                if smtp_config.get("tls"):
                    server.starttls()
                if smtp_config.get("user"):
                    server.login(smtp_config["user"], smtp_config["password"])
                server.sendmail(smtp_config["from"], [m.get("mail", "")], msg.as_string())
        except Exception as e:
            errors.append(f"{m.get('mail', '')}: {e}")

    if errors:
        QMessageBox.warning(parent, "Envoi partiel", "Certaines adresses ont échoué:\n" + "\n".join(errors))
    else:
        QMessageBox.information(parent, "Mailing", "Tous les mails ont été envoyés.")