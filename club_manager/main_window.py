# -*- coding: utf-8 -*-
"""
Fenêtre principale de Club Manager.
Gère l'orchestration des tabs, menus, dialogs, et la logique globale.
"""

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from club_manager.ui.members_tab import MembersTab
from club_manager.ui.positions_tab import PositionsTab
from club_manager.ui.sessions_tab import SessionsTab
from club_manager.ui.cotisations_tab import CotisationsTab
from club_manager.ui.custom_fields_tab import CustomFieldsTab
from club_manager.ui.audit_tab import AuditTab
from club_manager.ui.exports_tab import ExportsTab
from club_manager.ui.mailing_tab import MailingTab
from club_manager.ui.theming_tab import ThemingTab
from club_manager.ui.backup_tab import BackupTab
from club_manager.ui.about_dialog import AboutDialog
from club_manager.ui.welcome_dialog import WelcomeDialog
from club_manager.ui.tutorial_dialog import TutorialDialog
from club_manager.ui.doc_viewer_dialog import DocViewerDialog
from club_manager.core.theming import load_theme_choice, load_theme

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Club Manager")
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1200, 780)
        self.setup_tabs()        # Initialiser les tabs en premier !
        self.setup_menu()
        self.apply_theme_on_startup()
        self.show_welcome_if_first_launch()

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.members_tab = MembersTab()
        self.positions_tab = PositionsTab()
        self.sessions_tab = SessionsTab()
        self.cotisations_tab = CotisationsTab()
        self.custom_fields_tab = CustomFieldsTab()
        self.audit_tab = AuditTab()
        self.exports_tab = ExportsTab()
        self.mailing_tab = MailingTab()
        self.theming_tab = ThemingTab()
        self.backup_tab = BackupTab()

        self.tabs.addTab(self.members_tab, "Membres")
        self.tabs.addTab(self.positions_tab, "Postes")
        self.tabs.addTab(self.sessions_tab, "Sessions")
        self.tabs.addTab(self.cotisations_tab, "Cotisations")
        self.tabs.addTab(self.custom_fields_tab, "Champs personnalisés")
        self.tabs.addTab(self.exports_tab, "Exports")
        self.tabs.addTab(self.mailing_tab, "Mailing")
        self.tabs.addTab(self.audit_tab, "Audit")
        self.tabs.addTab(self.theming_tab, "Thème")
        self.tabs.addTab(self.backup_tab, "Sauvegarde")

    def setup_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&Fichier")
        help_menu = menu.addMenu("&Aide")

        action_backup = QAction("Exporter une sauvegarde...", self)
        action_backup.triggered.connect(self.backup_tab.start_backup)
        file_menu.addAction(action_backup)

        action_restore = QAction("Restaurer une sauvegarde...", self)
        action_restore.triggered.connect(self.backup_tab.start_restore)
        file_menu.addAction(action_restore)

        action_exit = QAction("Quitter", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        action_tutorial = QAction("Tutoriel interactif", self)
        action_tutorial.triggered.connect(self.show_tutorial)
        help_menu.addAction(action_tutorial)

        action_doc = QAction("Documentation", self)
        action_doc.triggered.connect(self.show_doc)
        help_menu.addAction(action_doc)

        action_about = QAction("À propos...", self)
        action_about.triggered.connect(self.show_about)
        help_menu.addAction(action_about)

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def show_tutorial(self):
        dialog = TutorialDialog(self)
        dialog.exec_()

    def show_doc(self):
        # On peut charger la doc HTML embarquée ici
        html = "<h2>Documentation Club Manager</h2><p>Consultez le README ou le Wiki pour plus d'infos.</p>"
        dialog = DocViewerDialog(self, html_content=html)
        dialog.exec_()

    def apply_theme_on_startup(self):
        qss, _ = load_theme_choice()
        if qss:
            load_theme(qss, self.parent() or self)

    def show_welcome_if_first_launch(self):
        # Logique simplifiée : afficher si pas de config, sinon passer
        import os
        if not os.path.exists("club_manager.conf"):
            dlg = WelcomeDialog(self)
            if dlg.exec_() == dlg.Accepted:
                # On pourrait sauvegarder les choix ici
                open("club_manager.conf", "w").close()
            else:
                self.close()