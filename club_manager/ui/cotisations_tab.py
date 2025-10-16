# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/cotisations_tab.py
Rôle : Onglet gestion des cotisations (CotisationsTab) du Club Manager.
Hérite de QWidget et de Ui_CotisationsTab.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_CotisationsTab généré par pyuic5 à partir de resources/ui/cotisations_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.cotisations_tab_ui import Ui_CotisationsTab

class CotisationsTab(QtWidgets.QWidget, Ui_CotisationsTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonAddCotisation.clicked.connect(self.add_cotisation)
        self.buttonEditCotisation.clicked.connect(self.edit_cotisation)
        self.buttonDeleteCotisation.clicked.connect(self.delete_cotisation)
        self.buttonExportCotisations.clicked.connect(self.export_cotisations)
        self.tableCotisations.doubleClicked.connect(self.edit_cotisation)
        self.buttonRelance.clicked.connect(self.relance_cotisation)

    def add_cotisation(self):
        from club_manager.ui.cotisation_form_dialog import CotisationFormDialog
        dlg = CotisationFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.refresh_cotisations()

    def edit_cotisation(self):
        # Logique de modification de la cotisation sélectionnée
        pass

    def delete_cotisation(self):
        # Logique de suppression de la/des cotisations sélectionnées
        pass

    def export_cotisations(self):
        # Exporter les cotisations
        pass

    def relance_cotisation(self):
        # Relancer les membres en retard de paiement
        pass

    def refresh_cotisations(self):
        # Recharge la table depuis la base
        pass