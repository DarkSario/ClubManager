# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/mailing_tab.py
Rôle : Onglet mailing (MailingTab) du Club Manager.
Hérite de QWidget et de Ui_MailingTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_MailingTab généré par pyuic5 à partir de resources/ui/mailing_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.mailing_tab_ui import Ui_MailingTab

class MailingTab(QtWidgets.QWidget, Ui_MailingTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonSendMail.clicked.connect(self.send_mail)
        self.buttonPreviewMail.clicked.connect(self.preview_mail)
        self.buttonSelectRecipients.clicked.connect(self.select_recipients)

    def send_mail(self):
        # Logique d'envoi de mail groupé
        # Vérifier que tous les champs sont remplis
        if not self.editSubject or not hasattr(self, 'editSubject'):
            QtWidgets.QMessageBox.warning(self, "Attention", "L'interface de mailing n'est pas complètement initialisée.")
            return
        
        subject = self.editSubject.text() if hasattr(self, 'editSubject') else ""
        body = self.textBody.toPlainText() if hasattr(self, 'textBody') else ""
        
        if not subject or not body:
            QtWidgets.QMessageBox.warning(self, "Attention", "Veuillez remplir le sujet et le corps du message.")
            return
        
        # Pour l'instant, juste un message d'information
        QtWidgets.QMessageBox.information(
            self,
            "Envoi de mail",
            "L'envoi de mail groupé nécessite la configuration d'un serveur SMTP.\n"
            "Cette fonctionnalité sera implémentée prochainement.\n\n"
            f"Sujet : {subject}\n"
            f"Corps : {body[:100]}..."
        )

    def preview_mail(self):
        # Afficher un aperçu du mail groupé
        subject = self.editSubject.text() if hasattr(self, 'editSubject') else ""
        body = self.textBody.toPlainText() if hasattr(self, 'textBody') else ""
        
        if not subject and not body:
            QtWidgets.QMessageBox.warning(self, "Attention", "Le sujet et le corps du message sont vides.")
            return
        
        # Afficher un aperçu
        preview = f"<h3>Aperçu du mail</h3>"
        preview += f"<p><strong>Sujet :</strong> {subject}</p>"
        preview += f"<p><strong>Corps :</strong></p>"
        preview += f"<p>{body.replace(chr(10), '<br>')}</p>"
        
        QtWidgets.QMessageBox.information(self, "Aperçu", preview)

    def select_recipients(self):
        # Sélectionner les destinataires (ouvre un dialog)
        from club_manager.ui.mailing_recipients_dialog import MailingRecipientsDialog
        
        try:
            dlg = MailingRecipientsDialog(self)
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                # Récupérer les destinataires sélectionnés
                QtWidgets.QMessageBox.information(
                    self,
                    "Destinataires",
                    "Les destinataires ont été sélectionnés.\n"
                    "Cette fonctionnalité sera pleinement opérationnelle prochainement."
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la sélection des destinataires : {str(e)}")