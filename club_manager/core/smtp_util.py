# -*- coding: utf-8 -*-
"""
Module utilitaire SMTP pour Club Manager.
Gère l'envoi d'emails via SMTP avec support TLS/SSL, batch sending, retry logic, et logging.
"""
import smtplib
import time
import os
from email.message import EmailMessage
from typing import List, Dict, Optional, Tuple
from cryptography.fernet import Fernet
import base64
import hashlib


class SMTPConfig:
    """Configuration SMTP avec chiffrement du mot de passe."""
    
    def __init__(self, host: str, port: int, security: str, username: str, 
                 password: str, from_address: str, reply_to: Optional[str] = None,
                 sender_name: Optional[str] = None, batch_size: int = 10,
                 batch_delay_ms: int = 1000, max_retries: int = 2,
                 enable_logging: bool = True):
        self.host = host
        self.port = port
        self.security = security  # 'none', 'starttls', 'ssl'
        self.username = username
        self.password = password
        self.from_address = from_address
        self.reply_to = reply_to or from_address
        self.sender_name = sender_name or from_address
        self.batch_size = batch_size
        self.batch_delay_ms = batch_delay_ms
        self.max_retries = max_retries
        self.enable_logging = enable_logging
    
    @staticmethod
    def get_encryption_key():
        """Récupère ou génère une clé de chiffrement basée sur APP_SECRET_KEY."""
        secret = os.environ.get('APP_SECRET_KEY', 'default-club-manager-key-change-in-production')
        # Dériver une clé Fernet valide (32 bytes base64) depuis le secret
        key = hashlib.sha256(secret.encode()).digest()
        return base64.urlsafe_b64encode(key)
    
    @staticmethod
    def encrypt_password(password: str) -> str:
        """Chiffre un mot de passe."""
        key = SMTPConfig.get_encryption_key()
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()
    
    @staticmethod
    def decrypt_password(encrypted: str) -> str:
        """Déchiffre un mot de passe."""
        key = SMTPConfig.get_encryption_key()
        f = Fernet(key)
        return f.decrypt(encrypted.encode()).decode()


class SMTPSender:
    """Gestionnaire d'envoi SMTP avec support batch et retry."""
    
    def __init__(self, config: SMTPConfig):
        self.config = config
        self.results = {
            'sent': [],
            'failed': []
        }
    
    def _connect_smtp(self):
        """Établit une connexion SMTP selon la configuration."""
        if self.config.security == 'ssl':
            server = smtplib.SMTP_SSL(self.config.host, self.config.port, timeout=30)
        else:
            server = smtplib.SMTP(self.config.host, self.config.port, timeout=30)
            if self.config.security == 'starttls':
                server.starttls()
        
        if self.config.username and self.config.password:
            server.login(self.config.username, self.config.password)
        
        return server
    
    def test_connection(self) -> Tuple[bool, str]:
        """Teste la connexion SMTP."""
        try:
            server = self._connect_smtp()
            server.quit()
            return True, "Connexion SMTP réussie"
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Erreur d'authentification: {str(e)}"
        except smtplib.SMTPException as e:
            return False, f"Erreur SMTP: {str(e)}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    def send_test_email(self, to_address: str) -> Tuple[bool, str]:
        """Envoie un email de test."""
        subject = "Test de configuration SMTP - Club Manager"
        body = "Ceci est un email de test envoyé depuis Club Manager.\n\nSi vous recevez ce message, votre configuration SMTP est correcte."
        
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = f"{self.config.sender_name} <{self.config.from_address}>"
            msg['To'] = to_address
            msg['Reply-To'] = self.config.reply_to
            msg.set_content(body)
            
            server = self._connect_smtp()
            server.send_message(msg)
            server.quit()
            
            return True, "Email de test envoyé avec succès"
        except Exception as e:
            return False, f"Erreur lors de l'envoi du test: {str(e)}"
    
    def send_bulk_email(self, subject: str, body: str, recipients: List[Dict[str, str]], 
                        progress_callback=None) -> Dict:
        """
        Envoie un email en masse à une liste de destinataires.
        
        Args:
            subject: Sujet de l'email
            body: Corps de l'email
            recipients: Liste de dicts avec 'email', 'first_name', 'last_name', 'id'
            progress_callback: Fonction de callback pour le progrès (current, total)
        
        Returns:
            Dict avec 'sent' (liste des réussites) et 'failed' (liste des échecs)
        """
        self.results = {'sent': [], 'failed': []}
        total = len(recipients)
        
        # Envoyer par lots
        for i in range(0, total, self.config.batch_size):
            batch = recipients[i:i + self.config.batch_size]
            
            for recipient in batch:
                success = self._send_single_email(subject, body, recipient)
                
                if progress_callback:
                    current = i + batch.index(recipient) + 1
                    progress_callback(current, total)
            
            # Délai entre les lots
            if i + self.config.batch_size < total:
                time.sleep(self.config.batch_delay_ms / 1000.0)
        
        return self.results
    
    def _send_single_email(self, subject: str, body: str, recipient: Dict[str, str]) -> bool:
        """Envoie un email à un seul destinataire avec retry."""
        email = recipient['email']
        
        for attempt in range(self.config.max_retries + 1):
            try:
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = f"{self.config.sender_name} <{self.config.from_address}>"
                msg['To'] = email
                msg['Reply-To'] = self.config.reply_to
                msg.set_content(body)
                
                server = self._connect_smtp()
                server.send_message(msg)
                server.quit()
                
                # Succès
                self.results['sent'].append({
                    'recipient_id': recipient.get('id'),
                    'email': email,
                    'name': f"{recipient.get('first_name', '')} {recipient.get('last_name', '')}".strip()
                })
                
                # Logger si activé
                if self.config.enable_logging:
                    self._log_send(recipient, subject, 'sent', None)
                
                return True
                
            except Exception as e:
                if attempt < self.config.max_retries:
                    time.sleep(1)  # Attendre 1 seconde avant retry
                    continue
                else:
                    # Échec définitif
                    error_msg = str(e)
                    self.results['failed'].append({
                        'recipient_id': recipient.get('id'),
                        'email': email,
                        'name': f"{recipient.get('first_name', '')} {recipient.get('last_name', '')}".strip(),
                        'error': error_msg
                    })
                    
                    # Logger si activé
                    if self.config.enable_logging:
                        self._log_send(recipient, subject, 'failed', error_msg)
                    
                    return False
    
    def _log_send(self, recipient: Dict, subject: str, status: str, error: Optional[str]):
        """Enregistre l'envoi dans la table mailing_logs."""
        try:
            from club_manager.core.database import Database
            from datetime import datetime
            
            db = Database.instance()
            cursor = db.connection.cursor()
            
            cursor.execute("""
                INSERT INTO mailing_logs (recipient_id, recipient_email, subject, status, error, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                recipient.get('id'),
                recipient['email'],
                subject,
                status,
                error,
                datetime.now().isoformat()
            ))
            
            db.connection.commit()
        except Exception as e:
            # Ne pas faire échouer l'envoi si le logging échoue
            print(f"Erreur lors du logging: {e}")


def get_smtp_config_from_db() -> Optional[SMTPConfig]:
    """Récupère la configuration SMTP depuis la base de données."""
    try:
        from club_manager.core.database import Database
        
        db = Database.instance()
        cursor = db.connection.cursor()
        
        # Récupérer tous les paramètres SMTP
        cursor.execute("SELECT key, value FROM settings WHERE key LIKE 'smtp_%'")
        settings = {row[0]: row[1] for row in cursor.fetchall()}
        
        if not settings.get('smtp_host'):
            return None
        
        # Déchiffrer le mot de passe
        password = settings.get('smtp_password', '')
        if password:
            try:
                password = SMTPConfig.decrypt_password(password)
            except:
                password = ''
        
        return SMTPConfig(
            host=settings.get('smtp_host', ''),
            port=int(settings.get('smtp_port', 587)),
            security=settings.get('smtp_security', 'starttls'),
            username=settings.get('smtp_username', ''),
            password=password,
            from_address=settings.get('smtp_from', ''),
            reply_to=settings.get('smtp_reply_to', ''),
            sender_name=settings.get('smtp_sender_name', ''),
            batch_size=int(settings.get('smtp_batch_size', 10)),
            batch_delay_ms=int(settings.get('smtp_batch_delay', 1000)),
            max_retries=int(settings.get('smtp_max_retries', 2)),
            enable_logging=settings.get('smtp_enable_logging', 'true') == 'true'
        )
    except Exception:
        return None


def save_smtp_config_to_db(config: SMTPConfig) -> bool:
    """Enregistre la configuration SMTP dans la base de données."""
    try:
        from club_manager.core.database import Database
        
        db = Database.instance()
        cursor = db.connection.cursor()
        
        # Chiffrer le mot de passe
        encrypted_password = SMTPConfig.encrypt_password(config.password) if config.password else ''
        
        settings = {
            'smtp_host': config.host,
            'smtp_port': str(config.port),
            'smtp_security': config.security,
            'smtp_username': config.username,
            'smtp_password': encrypted_password,
            'smtp_from': config.from_address,
            'smtp_reply_to': config.reply_to,
            'smtp_sender_name': config.sender_name,
            'smtp_batch_size': str(config.batch_size),
            'smtp_batch_delay': str(config.batch_delay_ms),
            'smtp_max_retries': str(config.max_retries),
            'smtp_enable_logging': 'true' if config.enable_logging else 'false'
        }
        
        for key, value in settings.items():
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            """, (key, value))
        
        db.connection.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la config SMTP: {e}")
        return False
