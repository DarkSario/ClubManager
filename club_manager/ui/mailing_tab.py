from PyQt5 import QtWidgets, QtCore
from club_manager.ui.mailing_tab_ui import Ui_MailingTab

class MailingTab(QtWidgets.QWidget, Ui_MailingTab):
    """Onglet de gestion des mailings groupés."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._selected_recipients = []

        self.buttonSendMail.clicked.connect(self.send_mail)
        self.buttonPreviewMail.clicked.connect(self.preview_mail)
        self.buttonSelectRecipients.clicked.connect(self.select_recipients)

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

        # Confirmation
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation d'envoi",
            f"Êtes-vous sûr de vouloir envoyer ce mail à {len(self._selected_recipients)} destinataire(s) ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QMessageBox.information(
                self,
                "Mailing",
                f"L'envoi de mails groupés nécessite une configuration SMTP.\n"
                f"Cette fonctionnalité sera disponible dans une prochaine version.\n\n"
                f"Destinataires sélectionnés : {len(self._selected_recipients)}"
            )

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
            members_with_email = [m for m in members if m.get('mail')]

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
