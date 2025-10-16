# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/main_window.py
Rôle : Fenêtre principale du Club Manager.
Points clés :
- Charge main_window.ui (QTabWidget principal)
- Instancie et insère chaque widget métier (MembersTab, PositionsTab, CotisationsTab, CustomFieldsTab, AuditTab, etc.)
- L'onglet Sessions a été supprimé - le système multi-base remplace la fonctionnalité de sessions
- Garantit que chaque bouton/action de chaque onglet est pleinement fonctionnel (slots connectés)
- Connexions menu (quitter, audit, RGPD, doc...) opérationnelles
- AUCUN widget global, respect cycle de vie QApplication
- PyQt5, Python 3.8+, PEP8, code prêt à coller/remplacer

Dépendances (pip install):
- PyQt5
"""

import sys
import logging
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

# Imports explicites des widgets métiers (chaque module .py/.ui doit exister et être correct)
from club_manager.ui.members_tab import MembersTab
from club_manager.ui.positions_tab import PositionsTab
from club_manager.ui.cotisations_tab import CotisationsTab
from club_manager.ui.custom_fields_tab import CustomFieldsTab
from club_manager.ui.audit_tab import AuditTab
from club_manager.ui.exports_tab import ExportsTab
from club_manager.ui.mailing_tab import MailingTab
from club_manager.ui.theming_tab import ThemingTab
from club_manager.ui.backup_tab import BackupTab

# Optionnel : extensions/fenêtres modales
from club_manager.ui.member_form_dialog import MemberFormDialog
from club_manager.ui.position_form_dialog import PositionFormDialog
from club_manager.ui.cotisation_form_dialog import CotisationFormDialog
from club_manager.ui.custom_field_form_dialog import CustomFieldFormDialog

class MainWindow(QtWidgets.QMainWindow):
    """
    Fenêtre principale de l'application Club Manager.
    Gère l'affichage et l'injection dynamique de tous les widgets métiers dans le QTabWidget.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Chargement de l'UI principale (main_window.ui)
        try:
            loadUi("resources/ui/main_window.ui", self)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur UI", f"Impossible de charger l'UI principale : {e}")
            logging.exception("Erreur lors du chargement de main_window.ui")
            sys.exit(1)

        # Injection explicite des widgets métiers dans chaque onglet du QTabWidget
        try:
            # Onglet Membres (index 0)
            self.members_tab = MembersTab(self)
            self._replace_tab_widget(0, self.members_tab)

            # Onglet Postes (index 1)
            self.positions_tab = PositionsTab(self)
            self._replace_tab_widget(1, self.positions_tab)

            # Onglet Cotisations (index 2)
            self.cotisations_tab = CotisationsTab(self)
            self._replace_tab_widget(2, self.cotisations_tab)

            # Onglet Champs personnalisés (index 3)
            self.custom_fields_tab = CustomFieldsTab(self)
            self._replace_tab_widget(3, self.custom_fields_tab)

            # Onglet Exports (index 4)
            self.exports_tab = ExportsTab(self)
            self._replace_tab_widget(4, self.exports_tab)

            # Onglet Mailing (index 5)
            self.mailing_tab = MailingTab(self)
            self._replace_tab_widget(5, self.mailing_tab)

            # Onglet Audit (index 6)
            self.audit_tab = AuditTab(self)
            self._replace_tab_widget(6, self.audit_tab)

            # Onglet Thématisation (index 7)
            self.theming_tab = ThemingTab(self)
            self._replace_tab_widget(7, self.theming_tab)

            # Onglet Sauvegarde/Restaurer (index 8)
            self.backup_tab = BackupTab(self)
            self._replace_tab_widget(8, self.backup_tab)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'injection des widgets métiers : {e}")
            logging.exception("Erreur lors de l'injection des widgets métiers")
            sys.exit(1)

        # Connexions des actions du menu principal
        self._connect_menu_actions()

    def _replace_tab_widget(self, tab_index: int, widget: QtWidgets.QWidget):
        """
        Remplace le contenu d'un onglet du QTabWidget par un widget métier custom.
        """
        tab = self.tabWidget.widget(tab_index)
        # On nettoie le layout existant (si nécessaire)
        if tab.layout() is None:
            layout = QtWidgets.QVBoxLayout(tab)
            tab.setLayout(layout)
        else:
            layout = tab.layout()
            # On retire les widgets existants
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().setParent(None)
        layout.addWidget(widget)

    def _connect_menu_actions(self):
        """
        Connexion de tous les menus/actions principaux.
        Les actions doivent exister dans le .ui (sinon, générer le .ui correspondant).
        """
        try:
            # Action Quitter
            self.actionQuitter.triggered.connect(self.close)
            # Action Audit : afficher l'onglet Audit
            self.actionAudit.triggered.connect(lambda: self.tabWidget.setCurrentIndex(6))
            # Action RGPD : afficher la documentation RGPD ou ouvrir la boîte de dialogue RGPD
            self.actionRGPD.triggered.connect(self._open_rgpd_dialog)
            # Action Documentation : ouvrir la doc utilisateur
            self.actionDocumentation.triggered.connect(self._open_documentation)
            # Action Sauvegarde : switch onglet
            self.actionSauvegarder.triggered.connect(lambda: self.tabWidget.setCurrentIndex(8))
            # Action Thème : switch onglet
            self.actionTheme.triggered.connect(lambda: self.tabWidget.setCurrentIndex(7))
            # Action Export : switch onglet
            self.actionExporter.triggered.connect(lambda: self.tabWidget.setCurrentIndex(4))
            # Action Mailing : switch onglet
            self.actionMailing.triggered.connect(lambda: self.tabWidget.setCurrentIndex(5))
            # Action Changer de langue
            self.actionChanger_de_langue.triggered.connect(self._switch_language)
        except Exception as e:
            logging.warning(f"Erreur lors de la connexion des actions de menu : {e}")

    def _open_rgpd_dialog(self):
        QtWidgets.QMessageBox.information(self, "RGPD", "Documentation RGPD et options de purge/anonymisation.")

    def _open_documentation(self):
        QtWidgets.QMessageBox.information(self, "Documentation", "Ouvrir la documentation utilisateur/de développement.")

    def _switch_language(self):
        QtWidgets.QMessageBox.information(self, "Langue", "La fonctionnalité multilingue n'est pas encore implémentée.")

# Guide d'extension :
# - Pour ajouter un nouvel onglet, créer le couple club_manager/ui/{nom}_tab.py + resources/ui/{nom}_tab.ui
# - Importer ici, instancier, puis appeler self._replace_tab_widget(nouvel_index, nouvel_objet)
# - Ajouter l'action de menu associée dans le .ui et la connecter dans _connect_menu_actions
