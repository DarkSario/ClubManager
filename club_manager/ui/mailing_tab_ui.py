# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/mailing_tab.ui
Classe : Ui_MailingTab
"""

from PyQt5 import QtWidgets, QtCore

class Ui_MailingTab(object):
    def setupUi(self, MailingTab):
        MailingTab.setObjectName("MailingTab")
        MailingTab.resize(700, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(MailingTab)
        self.horizontalLayoutTop = QtWidgets.QHBoxLayout()
        self.buttonSendMail = QtWidgets.QPushButton(MailingTab)
        self.buttonSendMail.setText("Envoyer")
        self.buttonPreviewMail = QtWidgets.QPushButton(MailingTab)
        self.buttonPreviewMail.setText("Prévisualiser")
        self.buttonSelectRecipients = QtWidgets.QPushButton(MailingTab)
        self.buttonSelectRecipients.setText("Sélection destinataires")
        self.horizontalLayoutTop.addWidget(self.buttonSendMail)
        self.horizontalLayoutTop.addWidget(self.buttonPreviewMail)
        self.horizontalLayoutTop.addWidget(self.buttonSelectRecipients)
        self.verticalLayout.addLayout(self.horizontalLayoutTop)
        self.textEditMail = QtWidgets.QTextEdit(MailingTab)
        self.textEditMail.setPlaceholderText("Rédigez votre message ici...")
        self.verticalLayout.addWidget(self.textEditMail)