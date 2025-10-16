# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/mailing_recipients_dialog.ui
Classe : Ui_MailingRecipientsDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_MailingRecipientsDialog(object):
    def setupUi(self, MailingRecipientsDialog):
        MailingRecipientsDialog.setObjectName("MailingRecipientsDialog")
        MailingRecipientsDialog.resize(400, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(MailingRecipientsDialog)
        self.labelInfo = QtWidgets.QLabel(MailingRecipientsDialog)
        self.labelInfo.setText("Sélectionnez les destinataires du mailing :")
        self.verticalLayout.addWidget(self.labelInfo)
        self.listRecipients = QtWidgets.QListWidget(MailingRecipientsDialog)
        self.listRecipients.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.verticalLayout.addWidget(self.listRecipients)
        self.buttonBox = QtWidgets.QDialogButtonBox(MailingRecipientsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)