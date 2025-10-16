# -*- coding: utf-8 -*-
"""
Fichier généré par pyuic5 à partir de resources/ui/doc_viewer_dialog.ui
Classe : Ui_DocViewerDialog
"""

from PyQt5 import QtWidgets, QtCore

class Ui_DocViewerDialog(object):
    def setupUi(self, DocViewerDialog):
        DocViewerDialog.setObjectName("DocViewerDialog")
        DocViewerDialog.resize(600, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(DocViewerDialog)
        self.textBrowser = QtWidgets.QTextBrowser(DocViewerDialog)
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtWidgets.QDialogButtonBox(DocViewerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)