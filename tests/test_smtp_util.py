# -*- coding: utf-8 -*-
"""
Tests unitaires pour le module SMTP (smtp_util.py).
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le chemin du module au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from club_manager.core.smtp_util import SMTPConfig, SMTPSender


class TestSMTPConfig(unittest.TestCase):
    """Tests pour la classe SMTPConfig."""
    
    def test_encrypt_decrypt_password(self):
        """Test du chiffrement et déchiffrement du mot de passe."""
        password = "my_secret_password_123"
        
        # Chiffrer
        encrypted = SMTPConfig.encrypt_password(password)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, password)
        
        # Déchiffrer
        decrypted = SMTPConfig.decrypt_password(encrypted)
        self.assertEqual(decrypted, password)
    
    def test_config_creation(self):
        """Test de création d'une configuration SMTP."""
        config = SMTPConfig(
            host="smtp.example.com",
            port=587,
            security="starttls",
            username="user@example.com",
            password="password123",
            from_address="noreply@example.com",
            sender_name="Test Sender"
        )
        
        self.assertEqual(config.host, "smtp.example.com")
        self.assertEqual(config.port, 587)
        self.assertEqual(config.security, "starttls")
        self.assertEqual(config.username, "user@example.com")
        self.assertEqual(config.batch_size, 10)  # valeur par défaut
        self.assertEqual(config.max_retries, 2)  # valeur par défaut


class TestSMTPSender(unittest.TestCase):
    """Tests pour la classe SMTPSender."""
    
    def setUp(self):
        """Initialisation avant chaque test."""
        self.config = SMTPConfig(
            host="smtp.example.com",
            port=587,
            security="starttls",
            username="user@example.com",
            password="password123",
            from_address="noreply@example.com",
            sender_name="Test Sender",
            batch_size=5,
            batch_delay_ms=100
        )
        self.sender = SMTPSender(self.config)
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_connect_smtp_starttls(self, mock_smtp):
        """Test de connexion SMTP avec STARTTLS."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        server = self.sender._connect_smtp()
        
        # Vérifier que SMTP a été appelé avec les bons paramètres
        mock_smtp.assert_called_once_with("smtp.example.com", 587, timeout=30)
        
        # Vérifier que starttls et login ont été appelés
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password123")
        
        self.assertEqual(server, mock_server)
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP_SSL')
    def test_connect_smtp_ssl(self, mock_smtp_ssl):
        """Test de connexion SMTP avec SSL."""
        config_ssl = SMTPConfig(
            host="smtp.example.com",
            port=465,
            security="ssl",
            username="user@example.com",
            password="password123",
            from_address="noreply@example.com"
        )
        sender_ssl = SMTPSender(config_ssl)
        
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server
        
        server = sender_ssl._connect_smtp()
        
        # Vérifier que SMTP_SSL a été appelé
        mock_smtp_ssl.assert_called_once_with("smtp.example.com", 465, timeout=30)
        
        # Vérifier que starttls n'a PAS été appelé (car SSL)
        mock_server.starttls.assert_not_called()
        
        # Vérifier que login a été appelé
        mock_server.login.assert_called_once_with("user@example.com", "password123")
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_test_connection_success(self, mock_smtp):
        """Test de test_connection avec succès."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        success, message = self.sender.test_connection()
        
        self.assertTrue(success)
        self.assertIn("réussie", message.lower())
        mock_server.quit.assert_called_once()
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_test_connection_auth_error(self, mock_smtp):
        """Test de test_connection avec erreur d'authentification."""
        mock_smtp.side_effect = Exception("Authentication failed")
        
        success, message = self.sender.test_connection()
        
        self.assertFalse(success)
        self.assertIn("erreur", message.lower())
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_send_test_email(self, mock_smtp):
        """Test d'envoi d'email de test."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        success, message = self.sender.send_test_email("test@example.com")
        
        self.assertTrue(success)
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    @patch('club_manager.core.smtp_util.time.sleep')
    def test_send_bulk_email(self, mock_sleep, mock_smtp):
        """Test d'envoi en masse."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        recipients = [
            {'id': 1, 'email': 'user1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'id': 2, 'email': 'user2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'id': 3, 'email': 'user3@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
        ]
        
        results = self.sender.send_bulk_email(
            subject="Test Subject",
            body="Test Body",
            recipients=recipients
        )
        
        # Vérifier que tous les emails ont été envoyés
        self.assertEqual(len(results['sent']), 3)
        self.assertEqual(len(results['failed']), 0)
        
        # Vérifier le nombre d'appels
        self.assertEqual(mock_server.send_message.call_count, 3)
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_send_single_email_with_retry(self, mock_smtp):
        """Test d'envoi avec retry en cas d'échec."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Simuler un échec puis un succès
        mock_server.send_message.side_effect = [
            Exception("Temporary error"),
            None  # Succès au 2ème essai
        ]
        
        recipient = {'id': 1, 'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
        
        success = self.sender._send_single_email("Subject", "Body", recipient)
        
        self.assertTrue(success)
        self.assertEqual(mock_server.send_message.call_count, 2)
    
    @patch('club_manager.core.smtp_util.smtplib.SMTP')
    def test_send_single_email_max_retries(self, mock_smtp):
        """Test d'échec définitif après max_retries."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Simuler des échecs constants
        mock_server.send_message.side_effect = Exception("Permanent error")
        
        recipient = {'id': 1, 'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
        
        success = self.sender._send_single_email("Subject", "Body", recipient)
        
        self.assertFalse(success)
        # max_retries = 2, donc 3 essais au total (initial + 2 retries)
        self.assertEqual(mock_server.send_message.call_count, 3)
        
        # Vérifier que l'échec est enregistré
        self.assertEqual(len(self.sender.results['failed']), 1)
        self.assertEqual(self.sender.results['failed'][0]['email'], 'test@example.com')


class TestSMTPConfigDatabase(unittest.TestCase):
    """Tests pour les fonctions de sauvegarde/chargement de config SMTP."""
    
    @patch('club_manager.core.database.Database')
    def test_save_smtp_config_to_db(self, mock_db_class):
        """Test de sauvegarde de la configuration."""
        from club_manager.core.smtp_util import save_smtp_config_to_db
        
        # Mock de la base de données
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.cursor.return_value = mock_cursor
        mock_db_class.instance.return_value = mock_db
        
        config = SMTPConfig(
            host="smtp.example.com",
            port=587,
            security="starttls",
            username="user@example.com",
            password="password123",
            from_address="noreply@example.com"
        )
        
        result = save_smtp_config_to_db(config)
        
        self.assertTrue(result)
        # Vérifier que execute a été appelé pour chaque paramètre
        self.assertGreater(mock_cursor.execute.call_count, 0)
        mock_db.connection.commit.assert_called_once()
    
    @patch('club_manager.core.database.Database')
    def test_get_smtp_config_from_db(self, mock_db_class):
        """Test de récupération de la configuration."""
        from club_manager.core.smtp_util import get_smtp_config_from_db
        
        # Mock de la base de données
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.cursor.return_value = mock_cursor
        mock_db_class.instance.return_value = mock_db
        
        # Simuler des paramètres dans la base
        encrypted_password = SMTPConfig.encrypt_password("password123")
        mock_cursor.fetchall.return_value = [
            ('smtp_host', 'smtp.example.com'),
            ('smtp_port', '587'),
            ('smtp_security', 'starttls'),
            ('smtp_username', 'user@example.com'),
            ('smtp_password', encrypted_password),
            ('smtp_from', 'noreply@example.com'),
        ]
        
        config = get_smtp_config_from_db()
        
        self.assertIsNotNone(config)
        self.assertEqual(config.host, 'smtp.example.com')
        self.assertEqual(config.port, 587)
        self.assertEqual(config.security, 'starttls')
        self.assertEqual(config.password, 'password123')  # Déchiffré


if __name__ == '__main__':
    unittest.main()
