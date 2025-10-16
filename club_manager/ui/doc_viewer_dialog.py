# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/doc_viewer_dialog.py
Rôle : Fenêtre modale de visualisation de la documentation embarquée.
Hérite de QDialog et Ui_DocViewerDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_DocViewerDialog généré par pyuic5 à partir de resources/ui/doc_viewer_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.doc_viewer_dialog_ui import Ui_DocViewerDialog

class DocViewerDialog(QtWidgets.QDialog, Ui_DocViewerDialog):
    def __init__(self, parent=None, html_content=""):
        super().__init__(parent)
        self.setupUi(self)
        self.textBrowser.setHtml(html_content)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)