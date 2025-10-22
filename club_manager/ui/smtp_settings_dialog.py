# -*- coding: utf-8 -*-
"""
Dialogue de configuration SMTP pour Club Manager.
Permet de configurer les paramètres d'envoi d'emails.
"""
from PyQt5 import QtWidgets, QtCore
from club_manager.core.smtp_util import SMTPConfig, SMTPSender, get_smtp_config_from_db, save_smtp_config_to_db


class SMTPSettingsDialog(QtWidgets.QDialog):
    """Dialogue de configuration des paramètres SMTP."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration SMTP")
        self.setModal(True)
        self.resize(600, 550)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Groupe Serveur
        server_group = QtWidgets.QGroupBox("Serveur SMTP")
        server_layout = QtWidgets.QFormLayout()
        
        self.edit_host = QtWidgets.QLineEdit()
        self.edit_host.setPlaceholderText("smtp.example.com")
        server_layout.addRow("Hôte SMTP:", self.edit_host)
        
        self.edit_port = QtWidgets.QSpinBox()
        self.edit_port.setRange(1, 65535)
        self.edit_port.setValue(587)
        server_layout.addRow("Port:", self.edit_port)
        
        self.combo_security = QtWidgets.QComboBox()
        self.combo_security.addItems(["Aucune", "STARTTLS", "SSL/TLS"])
        self.combo_security.setCurrentIndex(1)  # STARTTLS par défaut
        server_layout.addRow("Sécurité:", self.combo_security)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Groupe Authentification
        auth_group = QtWidgets.QGroupBox("Authentification")
        auth_layout = QtWidgets.QFormLayout()
        
        self.edit_username = QtWidgets.QLineEdit()
        self.edit_username.setPlaceholderText("utilisateur@example.com")
        auth_layout.addRow("Nom d'utilisateur:", self.edit_username)
        
        self.edit_password = QtWidgets.QLineEdit()
        self.edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_password.setPlaceholderText("Mot de passe")
        auth_layout.addRow("Mot de passe:", self.edit_password)
        
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        # Groupe Expéditeur
        sender_group = QtWidgets.QGroupBox("Informations expéditeur")
        sender_layout = QtWidgets.QFormLayout()
        
        self.edit_from = QtWidgets.QLineEdit()
        self.edit_from.setPlaceholderText("noreply@example.com")
        sender_layout.addRow("Adresse email:", self.edit_from)
        
        self.edit_sender_name = QtWidgets.QLineEdit()
        self.edit_sender_name.setPlaceholderText("Club Manager")
        sender_layout.addRow("Nom expéditeur:", self.edit_sender_name)
        
        self.edit_reply_to = QtWidgets.QLineEdit()
        self.edit_reply_to.setPlaceholderText("Laisser vide pour utiliser l'adresse email")
        sender_layout.addRow("Répondre à:", self.edit_reply_to)
        
        sender_group.setLayout(sender_layout)
        layout.addWidget(sender_group)
        
        # Groupe Paramètres d'envoi
        send_group = QtWidgets.QGroupBox("Paramètres d'envoi")
        send_layout = QtWidgets.QFormLayout()
        
        self.spin_batch_size = QtWidgets.QSpinBox()
        self.spin_batch_size.setRange(1, 100)
        self.spin_batch_size.setValue(10)
        send_layout.addRow("Taille du lot:", self.spin_batch_size)
        
        self.spin_batch_delay = QtWidgets.QSpinBox()
        self.spin_batch_delay.setRange(0, 10000)
        self.spin_batch_delay.setValue(1000)
        self.spin_batch_delay.setSuffix(" ms")
        send_layout.addRow("Délai entre lots:", self.spin_batch_delay)
        
        self.spin_max_retries = QtWidgets.QSpinBox()
        self.spin_max_retries.setRange(0, 5)
        self.spin_max_retries.setValue(2)
        send_layout.addRow("Tentatives max:", self.spin_max_retries)
        
        self.check_enable_logging = QtWidgets.QCheckBox("Activer les logs d'envoi")
        self.check_enable_logging.setChecked(True)
        send_layout.addRow("", self.check_enable_logging)
        
        send_group.setLayout(send_layout)
        layout.addWidget(send_group)
        
        # Note de sécurité
        note_label = QtWidgets.QLabel(
            "<i><b>Note de sécurité:</b> Le mot de passe est chiffré avec une clé dérivée de APP_SECRET_KEY. "
            "Pour une sécurité maximale en production, définissez une variable d'environnement APP_SECRET_KEY unique.</i>"
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("QLabel { color: #FF6F00; padding: 10px; }")
        layout.addWidget(note_label)
        
        # Boutons d'action
        button_layout = QtWidgets.QHBoxLayout()
        
        self.button_test = QtWidgets.QPushButton("Tester la connexion")
        self.button_test.clicked.connect(self.test_connection)
        button_layout.addWidget(self.button_test)
        
        self.button_test_email = QtWidgets.QPushButton("Envoyer un email de test")
        self.button_test_email.clicked.connect(self.send_test_email)
        button_layout.addWidget(self.button_test_email)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Boutons de dialogue
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_settings(self):
        """Charge les paramètres depuis la base de données."""
        config = get_smtp_config_from_db()
        if config:
            self.edit_host.setText(config.host)
            self.edit_port.setValue(config.port)
            
            security_map = {'none': 0, 'starttls': 1, 'ssl': 2}
            self.combo_security.setCurrentIndex(security_map.get(config.security, 1))
            
            self.edit_username.setText(config.username)
            self.edit_password.setText(config.password)
            self.edit_from.setText(config.from_address)
            self.edit_sender_name.setText(config.sender_name)
            self.edit_reply_to.setText(config.reply_to if config.reply_to != config.from_address else '')
            
            self.spin_batch_size.setValue(config.batch_size)
            self.spin_batch_delay.setValue(config.batch_delay_ms)
            self.spin_max_retries.setValue(config.max_retries)
            self.check_enable_logging.setChecked(config.enable_logging)
    
    def get_config(self) -> SMTPConfig:
        """Récupère la configuration depuis le formulaire."""
        security_map = {0: 'none', 1: 'starttls', 2: 'ssl'}
        
        return SMTPConfig(
            host=self.edit_host.text().strip(),
            port=self.edit_port.value(),
            security=security_map[self.combo_security.currentIndex()],
            username=self.edit_username.text().strip(),
            password=self.edit_password.text(),
            from_address=self.edit_from.text().strip(),
            reply_to=self.edit_reply_to.text().strip() or self.edit_from.text().strip(),
            sender_name=self.edit_sender_name.text().strip() or self.edit_from.text().strip(),
            batch_size=self.spin_batch_size.value(),
            batch_delay_ms=self.spin_batch_delay.value(),
            max_retries=self.spin_max_retries.value(),
            enable_logging=self.check_enable_logging.isChecked()
        )
    
    def validate_form(self) -> bool:
        """Valide le formulaire."""
        if not self.edit_host.text().strip():
            QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "L'hôte SMTP est obligatoire.")
            self.edit_host.setFocus()
            return False
        
        if not self.edit_from.text().strip():
            QtWidgets.QMessageBox.warning(self, "Champ obligatoire", "L'adresse email est obligatoire.")
            self.edit_from.setFocus()
            return False
        
        return True
    
    def test_connection(self):
        """Teste la connexion SMTP."""
        if not self.validate_form():
            return
        
        config = self.get_config()
        sender = SMTPSender(config)
        
        # Afficher un dialogue de progression
        progress = QtWidgets.QProgressDialog("Test de connexion en cours...", None, 0, 0, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        QtCore.QTimer.singleShot(100, lambda: self._do_test_connection(sender, progress))
    
    def _do_test_connection(self, sender, progress):
        """Effectue le test de connexion."""
        success, message = sender.test_connection()
        progress.close()
        
        if success:
            QtWidgets.QMessageBox.information(self, "Test réussi", message)
        else:
            QtWidgets.QMessageBox.critical(self, "Test échoué", message)
    
    def send_test_email(self):
        """Envoie un email de test."""
        if not self.validate_form():
            return
        
        # Demander l'adresse de test
        test_email, ok = QtWidgets.QInputDialog.getText(
            self,
            "Email de test",
            "Entrez l'adresse email où envoyer le test:",
            QtWidgets.QLineEdit.Normal,
            self.edit_from.text()
        )
        
        if not ok or not test_email.strip():
            return
        
        config = self.get_config()
        sender = SMTPSender(config)
        
        # Afficher un dialogue de progression
        progress = QtWidgets.QProgressDialog("Envoi de l'email de test...", None, 0, 0, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        QtCore.QTimer.singleShot(100, lambda: self._do_send_test(sender, test_email, progress))
    
    def _do_send_test(self, sender, test_email, progress):
        """Effectue l'envoi du test."""
        success, message = sender.send_test_email(test_email)
        progress.close()
        
        if success:
            QtWidgets.QMessageBox.information(self, "Test réussi", message)
        else:
            QtWidgets.QMessageBox.critical(self, "Test échoué", message)
    
    def accept(self):
        """Valide et sauvegarde la configuration."""
        if not self.validate_form():
            return
        
        config = self.get_config()
        if save_smtp_config_to_db(config):
            QtWidgets.QMessageBox.information(
                self,
                "Configuration enregistrée",
                "La configuration SMTP a été enregistrée avec succès."
            )
            super().accept()
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Erreur",
                "Impossible d'enregistrer la configuration SMTP."
            )
