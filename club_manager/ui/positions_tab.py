# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/positions_tab.py
Rôle : Onglet gestion des postes (PositionsTab) du Club Manager.
Hérite de QWidget et de Ui_PositionsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_PositionsTab généré par pyuic5 à partir de resources/ui/positions_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.positions_tab_ui import Ui_PositionsTab

class PositionsTab(QtWidgets.QWidget, Ui_PositionsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddPosition.clicked.connect(self.add_position)
        self.buttonEditPosition.clicked.connect(self.edit_position)
        self.buttonDeletePosition.clicked.connect(self.delete_position)
        self.buttonExportPositions.clicked.connect(self.export_positions)
        self.tablePositions.doubleClicked.connect(self.edit_position)
        self.buttonAffect.clicked.connect(self.affect_position)
        self.buttonUnaffect.clicked.connect(self.unaffect_position)

    def add_position(self):
        from club_manager.ui.position_form_dialog import PositionFormDialog
        dlg = PositionFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_positions()

    def edit_position(self):
        # Logique de modification du poste sélectionné
        pass

    def delete_position(self):
        # Logique de suppression du/des postes sélectionnés
        pass

    def export_positions(self):
        # Exporter les postes
        pass

    def affect_position(self):
        # Affecter un poste à un membre
        pass

    def unaffect_position(self):
        # Désaffecter un poste d'un membre
        pass

    def refresh_positions(self):
        # Recharge la table depuis la base
        pass