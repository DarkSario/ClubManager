from PyQt5 import QtWidgets, QtCore
from club_manager.ui.mailing_tab_ui import Ui_MailingTab
from club_manager.ui.smtp_settings_dialog import SMTPSettingsDialog
from club_manager.core.smtp_util import get_smtp_config_from_db, SMTPSender

class MailingTab(QtWidgets.QWidget, Ui_MailingTab):
    """Onglet de gestion des mailings groupés."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._selected_recipients = []
        self._setup_additional_ui()

        self.buttonSendMail.clicked.connect(self.send_mail)
        self.buttonPreviewMail.clicked.connect(self.preview_mail)
        self.buttonSelectRecipients.clicked.connect(self.select_recipients)
        self.buttonSMTPSettings.clicked.connect(self.open_smtp_settings)
    
    def _setup_additional_ui(self):
        """Configure les éléments UI supplémentaires."""
        # Ajouter un bouton de configuration SMTP
        self.buttonSMTPSettings = QtWidgets.QPushButton("⚙ Configuration SMTP")
        self.layout().itemAt(0).layout().addWidget(self.buttonSMTPSettings)
        
        # Ajouter une aide
        help_text = QtWidgets.QLabel(
            "<i>📧 <b>Mailing groupé:</b> Sélectionnez les destinataires, rédigez votre message et envoyez. "
            "Les emails sont envoyés par lots pour éviter les limitations SMTP. "
            "Configurez d'abord les paramètres SMTP via le bouton de configuration.</i>"
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("QLabel { padding: 10px; background-color: #E3F2FD; border-radius: 5px; }")
        self.layout().insertWidget(1, help_text)
        
        # Ajouter une barre de progression
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout().insertWidget(2, self.progress_bar)
    
    def open_smtp_settings(self):
        """Ouvre le dialogue de configuration SMTP."""
        dialog = SMTPSettingsDialog(self)
        dialog.exec_()

    def send_mail(self):
        """Envoie un mail groupé aux destinataires sélectionnés."""
        if not self._selected_recipients:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucun destinataire",
                "Veuillez d'abord sélectionner les destinataires avec le bouton 'Sélectionner les destinataires'."
            )
            return

        # Validation des champs du formulaire
        if not self.editSubject.text():
            QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le sujet du mail est obligatoire.")
            return

        if not self.editBody.toPlainText():
            QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "Le corps du mail est obligatoire.")
            return
        
        # Vérifier la configuration SMTP
        config = get_smtp_config_from_db()
        if not config:
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Configuration SMTP manquante",
                "La configuration SMTP n'est pas définie. Voulez-vous la configurer maintenant ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.open_smtp_settings()
            return

        # Confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation d'envoi",
            f"Êtes-vous sûr de vouloir envoyer ce mail à {len(self._selected_recipients)} destinataire(s) ?\n\n"
            f"Sujet: {self.editSubject.text()}",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self._send_bulk_email(config)
    
    def _send_bulk_email(self, config):
        """Effectue l'envoi en masse avec barre de progression."""
        subject = self.editSubject.text()
        body = self.editBody.toPlainText()
        
        # Préparer la liste des destinataires
        recipients = [
            {
                'id': r.get('id'),
                'email': r['mail'],
                'first_name': r.get('first_name', ''),
                'last_name': r.get('last_name', '')
            }
            for r in self._selected_recipients
        ]
        
        # Afficher la barre de progression
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(recipients))
        self.progress_bar.setValue(0)
        
        # Désactiver les boutons pendant l'envoi
        self.buttonSendMail.setEnabled(False)
        self.buttonPreviewMail.setEnabled(False)
        self.buttonSelectRecipients.setEnabled(False)
        self.buttonSMTPSettings.setEnabled(False)
        
        # Créer le sender
        sender = SMTPSender(config)
        
        # Callback pour mettre à jour la progression
        def update_progress(current, total):
            self.progress_bar.setValue(current)
            QtCore.QCoreApplication.processEvents()
        
        # Envoyer dans un thread séparé (simulation avec QTimer pour simplifier)
        QtCore.QTimer.singleShot(100, lambda: self._do_send(sender, subject, body, recipients, update_progress))
    
    def _do_send(self, sender, subject, body, recipients, progress_callback):
        """Effectue l'envoi réel."""
        results = sender.send_bulk_email(subject, body, recipients, progress_callback)
        
        # Réactiver les boutons
        self.buttonSendMail.setEnabled(True)
        self.buttonPreviewMail.setEnabled(True)
        self.buttonSelectRecipients.setEnabled(True)
        self.buttonSMTPSettings.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Afficher le résumé
        self._show_send_results(results)

    def preview_mail(self):
        """Affiche un aperçu du mail groupé."""
        subject = self.editSubject.text()
        body = self.editBody.toPlainText()

        preview_text = f"<h3>Aperçu du mail</h3>"
        preview_text += f"<p><b>Sujet :</b> {subject}</p>"
        preview_text += f"<p><b>Corps :</b></p>"
        preview_text += f"<p>{body.replace(chr(10), '<br>')}</p>"
        preview_text += f"<p><b>Nombre de destinataires :</b> {len(self._selected_recipients)}</p>"

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Aperçu du mail")
        msg.setTextFormat(QtCore.Qt.RichText)  # Correction ici !
        msg.setText(preview_text)
        msg.exec_()

    def select_recipients(self):
        """Ouvre un dialogue pour sélectionner les destinataires."""
        from club_manager.core.members import get_all_members

        try:
            members = get_all_members()
            if not members:
                QtWidgets.QMessageBox.information(self, "Aucun membre", "Aucun membre disponible.")
                return

            # Filtrer les membres ayant un email
            members_with_email = [m for m in members if m['mail']]

            if not members_with_email:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Aucun email",
                    "Aucun membre n'a d'adresse email enregistrée."
                )
                return

            # Créer un dialogue de sélection multiple
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Sélectionner les destinataires")
            dialog.resize(400, 500)

            layout = QtWidgets.QVBoxLayout(dialog)

            label = QtWidgets.QLabel("Sélectionnez les membres à qui envoyer le mail :")
            layout.addWidget(label)

            list_widget = QtWidgets.QListWidget()
            list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

            for member in members_with_email:
                item_text = f"{member['last_name']} {member['first_name']} ({member['mail']})"
                item = QtWidgets.QListWidgetItem(item_text)
                item.setData(QtCore.Qt.UserRole, member)
                list_widget.addItem(item)

            layout.addWidget(list_widget)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self._selected_recipients = [
                    item.data(QtCore.Qt.UserRole)
                    for item in list_widget.selectedItems()
                ]
                QtWidgets.QMessageBox.information(
                    self,
                    "Sélection",
                    f"{len(self._selected_recipients)} destinataire(s) sélectionné(s)."
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la sélection : {str(e)}")
    
    def _show_send_results(self, results):
        """Affiche les résultats de l'envoi."""
        sent_count = len(results['sent'])
        failed_count = len(results['failed'])
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Résultats de l'envoi")
        
        if failed_count == 0:
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"✓ Tous les emails ont été envoyés avec succès !")
            msg.setInformativeText(f"{sent_count} destinataire(s) ont reçu le message.")
        else:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(f"Envoi terminé avec {failed_count} erreur(s)")
            msg.setInformativeText(
                f"• Envoyés: {sent_count}\n"
                f"• Échecs: {failed_count}"
            )
            
            # Détails des échecs
            if failed_count > 0:
                details = "Échecs d'envoi:\n\n"
                for failed in results['failed']:
                    details += f"• {failed['name']} ({failed['email']})\n  Erreur: {failed['error']}\n\n"
                msg.setDetailedText(details)
        
        msg.exec_()
