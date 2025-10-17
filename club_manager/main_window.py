# -*- coding: utf-8 -*-
"""
Fenêtre principale de Club Manager.
Gère l'orchestration des tabs, menus, dialogs, et la logique globale.
"""

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from club_manager.ui.members_tab import MembersTab
from club_manager.ui.positions_tab import PositionsTab
from club_manager.ui.mjc_clubs_tab import MJCClubsTab
# annual_prices_tab import removed
from club_manager.ui.audit_tab import AuditTab
from club_manager.ui.exports_tab import ExportsTab
from club_manager.ui.mailing_tab import MailingTab
from club_manager.ui.theming_tab import ThemingTab
from club_manager.ui.backup_tab import BackupTab
from club_manager.ui.about_dialog import AboutDialog
from club_manager.ui.welcome_dialog import WelcomeDialog
from club_manager.ui.tutorial_dialog import TutorialDialog
from club_manager.ui.doc_viewer_dialog import DocViewerDialog
from club_manager.ui.database_selector_dialog import DatabaseSelectorDialog
from club_manager.core.theming import load_theme_choice, load_theme
from club_manager.core.database import Database
import os

class MainWindow(QMainWindow):
    def __init__(self, db_path=None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        
        # Initialiser la base de données
        if self.db_path:
            Database.instance(self.db_path)
        
        self.setWindowTitle("Club Manager")
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1200, 780)
        self.setup_tabs()        # Initialiser les tabs en premier !
        self.setup_menu()
        self.apply_theme_on_startup()
        self.update_window_title()
        # Note: show_welcome_if_first_launch supprimé car remplacé par database_selector_dialog

    def update_window_title(self):
        """Met à jour le titre de la fenêtre avec le nom de la base."""
        if self.db_path:
            db_name = os.path.basename(self.db_path)
            self.setWindowTitle(f"Club Manager - {db_name}")
        else:
            self.setWindowTitle("Club Manager")

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.members_tab = MembersTab()
        self.positions_tab = PositionsTab()
        self.mjc_clubs_tab = MJCClubsTab()
        # annual_prices_tab removed as per requirements
        self.audit_tab = AuditTab()
        self.exports_tab = ExportsTab()
        self.mailing_tab = MailingTab()
        self.theming_tab = ThemingTab()
        self.backup_tab = BackupTab()

        self.tabs.addTab(self.members_tab, "Membres")
        self.tabs.addTab(self.positions_tab, "Postes")
        self.tabs.addTab(self.mjc_clubs_tab, "Clubs MJC")
        # Prix annuels tab removed
        self.tabs.addTab(self.exports_tab, "Exports")
        self.tabs.addTab(self.mailing_tab, "Mailing")
        self.tabs.addTab(self.audit_tab, "Audit")
        self.tabs.addTab(self.theming_tab, "Thème")
        self.tabs.addTab(self.backup_tab, "Sauvegarde")

    def setup_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&Fichier")
        help_menu = menu.addMenu("&Aide")

        action_change_db = QAction("Changer de base de données...", self)
        action_change_db.triggered.connect(self.change_database)
        file_menu.addAction(action_change_db)
        
        file_menu.addSeparator()
        
        action_modify_prices = QAction("Modifier les tarifs de l'année courante...", self)
        action_modify_prices.triggered.connect(self.modify_current_prices)
        file_menu.addAction(action_modify_prices)
        
        file_menu.addSeparator()

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
    
    def change_database(self):
        """Permet de changer de base de données."""
        reply = QMessageBox.question(
            self,
            "Changer de base de données",
            "Voulez-vous vraiment changer de base de données ?\n"
            "Toutes les modifications non sauvegardées seront perdues.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            db_selector = DatabaseSelectorDialog(self)
            if db_selector.exec_() == DatabaseSelectorDialog.Accepted:
                new_db_path = db_selector.get_selected_database_path()
                if new_db_path:
                    self.db_path = new_db_path
                    Database.change_database(self.db_path)
                    self.update_window_title()
                    # Rafraîchir tous les tabs
                    self.refresh_all_tabs()
                    QMessageBox.information(
                        self,
                        "Base changée",
                        f"La base de données a été changée avec succès."
                    )
    
    def refresh_all_tabs(self):
        """Rafraîchit tous les onglets après un changement de base."""
        try:
            self.members_tab.refresh_members()
        except:
            pass
        try:
            self.mjc_clubs_tab.refresh_clubs()
        except:
            pass
        # annual_prices_tab removed
        # Ajouter d'autres rafraîchissements si nécessaire
    
    def modify_current_prices(self):
        """Permet de modifier les tarifs de l'année courante avec un avertissement."""
        from club_manager.core.annual_prices import get_current_annual_price, update_annual_price
        from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QLabel
        
        # Récupérer les tarifs actuels
        current_price = get_current_annual_price()
        if not current_price:
            QMessageBox.warning(
                self,
                "Aucun tarif",
                "Aucun tarif n'est configuré pour cette base de données.\n"
                "Veuillez d'abord créer une configuration de tarifs."
            )
            return
        
        # Afficher un avertissement
        reply = QMessageBox.warning(
            self,
            "Modifier les tarifs",
            "⚠️ ATTENTION ⚠️\n\n"
            "Vous êtes sur le point de modifier les tarifs de l'année courante.\n"
            "Cette action peut affecter les cotisations des membres existants.\n\n"
            "Il est recommandé de :\n"
            "- Créer une nouvelle base pour une nouvelle saison\n"
            "- Ou de vérifier que cette modification est bien nécessaire\n\n"
            "Voulez-vous continuer ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Créer le dialogue de modification
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier les tarifs de l'année courante")
        dialog.setModal(True)
        
        layout = QFormLayout()
        
        # Informations
        info_label = QLabel(f"Modification des tarifs pour l'année : {current_price['year']}")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addRow(info_label)
        
        # Champs de saisie
        edit_year = QLineEdit(current_price['year'])
        layout.addRow("Année :", edit_year)
        
        edit_club_price = QLineEdit(str(current_price['club_price']))
        layout.addRow("Prix Club (€) :", edit_club_price)
        
        edit_mjc_price = QLineEdit(str(current_price['mjc_price']))
        layout.addRow("Prix MJC (€) :", edit_mjc_price)
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                year = edit_year.text().strip()
                club_price = float(edit_club_price.text().strip())
                mjc_price = float(edit_mjc_price.text().strip())
                
                if not year:
                    QMessageBox.warning(self, "Champ requis", "L'année est obligatoire.")
                    return
                
                if club_price < 0 or mjc_price < 0:
                    QMessageBox.warning(self, "Montant invalide", "Les prix ne peuvent pas être négatifs.")
                    return
                
                # Mettre à jour les tarifs
                update_annual_price(
                    current_price['id'],
                    year,
                    club_price,
                    mjc_price,
                    True  # Garder comme tarif courant
                )
                
                QMessageBox.information(
                    self,
                    "Succès",
                    "Les tarifs ont été modifiés avec succès."
                )
            except ValueError:
                QMessageBox.critical(self, "Erreur", "Les prix doivent être des nombres valides.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification : {str(e)}")

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def show_tutorial(self):
        dialog = TutorialDialog(self)
        dialog.exec_()

    def show_doc(self):
        """Affiche la documentation HTML embarquée."""
        import os
        # Charger la documentation HTML embarquée
        doc_path = os.path.join(os.path.dirname(__file__), "..", "resources", "docs", "user_manual.html")
        doc_path = os.path.abspath(doc_path)
        
        html_content = ""
        try:
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            else:
                html_content = """
                <h2>Documentation Club Manager</h2>
                <p>Le fichier de documentation n'a pas été trouvé.</p>
                <p>Consultez le README.md pour plus d'informations.</p>
                """
        except Exception as e:
            html_content = f"""
            <h2>Erreur</h2>
            <p>Impossible de charger la documentation : {str(e)}</p>
            <p>Consultez le README.md pour plus d'informations.</p>
            """
        
        dialog = DocViewerDialog(self, html_content=html_content)
        dialog.exec_()

    def apply_theme_on_startup(self):
        qss, _ = load_theme_choice()
        if qss:
            load_theme(qss, self.parent() or self)

