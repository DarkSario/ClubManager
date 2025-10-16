# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/mailing_recipients_dialog.py
Rôle : Fenêtre modale de sélection des destinataires du mailing.
Hérite de QDialog et Ui_MailingRecipientsDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_MailingRecipientsDialog généré par pyuic5 à partir de resources/ui/mailing_recipients_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.mailing_recipients_dialog_ui import Ui_MailingRecipientsDialog

class MailingRecipientsDialog(QtWidgets.QDialog, Ui_MailingRecipientsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # TODO: wiring logique sélection/désélection groupée si besoin