# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/export_fields_dialog.ui
Classe : Ui_ExportFieldsDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_ExportFieldsDialog(object):
    def setupUi(self, ExportFieldsDialog):
        ExportFieldsDialog.setObjectName("ExportFieldsDialog")
        ExportFieldsDialog.resize(350, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(ExportFieldsDialog)
        self.checkAllFields = QtWidgets.QCheckBox(ExportFieldsDialog)
        self.checkAllFields.setText("Tout sélectionner")
        self.verticalLayout.addWidget(self.checkAllFields)
        self.listFields = QtWidgets.QListWidget(ExportFieldsDialog)
        self.listFields.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.verticalLayout.addWidget(self.listFields)
        self.buttonBox = QtWidgets.QDialogButtonBox(ExportFieldsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)