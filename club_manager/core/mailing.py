# -*- coding: utf-8 -*-
"""
Module d'envoi de mailing groupé (SMTP) pour Club Manager.
Gère la sélection des destinataires, la composition du message, et l'envoi via SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QMessageBox

def send_mailing(subject, message, recipient_list, smtp_config, parent=None):
    try:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = smtp_config["from"]
        msg["To"] = ", ".join(recipient_list)
        with smtplib.SMTP(smtp_config["host"], smtp_config.get("port", 25)) as server:
            if smtp_config.get("tls"):
                server.starttls()
            if smtp_config.get("user"):
                server.login(smtp_config["user"], smtp_config["password"])
            server.sendmail(smtp_config["from"], recipient_list, msg.as_string())
        QMessageBox.information(parent, "Mailing", "Mail envoyé à tous les destinataires.")
    except Exception as e:
        QMessageBox.critical(parent, "Erreur SMTP", f"Erreur lors de l'envoi : {e}")