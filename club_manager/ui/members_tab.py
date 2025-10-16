# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/members_tab.py
Rôle : Onglet gestion des adhérents (MembersTab) du Club Manager.
Hérite de QWidget et de Ui_MembersTab.
Tous les boutons/actions sont connectés à des slots effectifs dans la classe.
Dépendances : PyQt5, Ui_MembersTab généré par pyuic5 à partir de resources/ui/members_tab.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.members_tab_ui import Ui_MembersTab

class MembersTab(QtWidgets.QWidget, Ui_MembersTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Connexion des boutons du tab à leur logique
        self.buttonAddMember.clicked.connect(self.add_member)
        self.buttonEditMember.clicked.connect(self.edit_member)
        self.buttonDeleteMember.clicked.connect(self.delete_member)
        self.buttonExportMembers.clicked.connect(self.export_members)
        self.buttonFilter.clicked.connect(self.filter_members)
        self.buttonResetFilter.clicked.connect(self.reset_filter)
        self.buttonMailing.clicked.connect(self.do_mailing)
        self.tableMembers.doubleClicked.connect(self.edit_member)
        # TODO : Connexions additionnelles selon les besoins

    def add_member(self):
        # Logique d'ajout d'un adhérent (ouvre le dialog)
        from club_manager.ui.member_form_dialog import MemberFormDialog
        dlg = MemberFormDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Ajout effectif du membre, recharge table
            self.refresh_members()
    
    def edit_member(self):
        # Logique de modification d'un adhérent sélectionné
        # TODO: Récupérer l'ID du membre sélectionné
        pass

    def delete_member(self):
        # Logique de suppression d'un ou plusieurs membres sélectionnés
        pass

    def export_members(self):
        # Logique d'export CSV/PDF de la liste actuelle
        pass

    def filter_members(self):
        # Logique de filtrage multicritère
        pass

    def reset_filter(self):
        # Réinitialise tous les filtres
        pass

    def do_mailing(self):
        # Lancer le module de mailing sur sélection
        pass

    def refresh_members(self):
        # Recharge la table depuis la base
        pass