# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/session_form_dialog.ui
Classe : Ui_SessionFormDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_SessionFormDialog(object):
    def setupUi(self, SessionFormDialog):
        SessionFormDialog.setObjectName("SessionFormDialog")
        SessionFormDialog.resize(400, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(SessionFormDialog)
        self.formLayout = QtWidgets.QFormLayout()
        self.editSessionName = QtWidgets.QLineEdit(SessionFormDialog)
        self.formLayout.addRow("Nom de la session :", self.editSessionName)
        self.dateStart = QtWidgets.QDateEdit(SessionFormDialog)
        self.dateStart.setCalendarPopup(True)
        self.formLayout.addRow("Date début :", self.dateStart)
        self.dateEnd = QtWidgets.QDateEdit(SessionFormDialog)
        self.dateEnd.setCalendarPopup(True)
        self.formLayout.addRow("Date fin :", self.dateEnd)
        self.editClubAmount = QtWidgets.QLineEdit(SessionFormDialog)
        self.formLayout.addRow("Part club :", self.editClubAmount)
        self.editMJCAmount = QtWidgets.QLineEdit(SessionFormDialog)
        self.formLayout.addRow("Part MJC :", self.editMJCAmount)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SessionFormDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)