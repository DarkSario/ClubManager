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
        pass

    def preview_mail(self):
        # Afficher un aperçu du mail groupé
        pass

    def select_recipients(self):
        # Sélectionner les destinataires (ouvre un dialog)
        pass