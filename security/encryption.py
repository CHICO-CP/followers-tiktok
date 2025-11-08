"""
Advanced Encryption and Security Management
"""

import os
import base64
import hashlib
import hmac
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional

class EncryptionManager:
    def __init__(self, key_file: str = "config/encryption.key"):
        self.key_file = key_file
        self.logger = logging.getLogger(__name__)
        self.cipher = self._initialize_cipher()
        
    def _initialize_cipher(self) -> Optional[Fernet]:
        """Initialize encryption cipher"""
        try:
            key = self._load_or_generate_key()
            if key:
                return Fernet(key)
            return None
        except Exception as e:
            self.logger.error(f"Cipher initialization failed: {e}")
            return None
            
    def _load_or_generate_key(self) -> Optional[bytes]:
        """Load existing key or generate new one"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    return f.read()
            else:
                # Generate new key
                key = Fernet.generate_key()
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
                
                # Save key
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                    
                self.logger.info("New encryption key generated and saved")
                return key
                
        except Exception as e:
            self.logger.error(f"Key management failed: {e}")
            return None
            
    def encrypt(self, data: str) -> Optional[str]:
        """Encrypt string data"""
        if not self.cipher:
            self.logger.error("Cipher not available for encryption")
            return None
            
        try:
            encrypted_data = self.cipher.encrypt(data.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            return None
            
    def decrypt(self, encrypted_data: str) -> Optional[str]:
        """Decrypt string data"""
        if not self.cipher:
            self.logger.error("Cipher not available for decryption")
            return None
            
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None
            
    def encrypt_credentials(self, username: str, password: str) -> Optional[Dict]:
        """Encrypt credentials with integrity check"""
        try:
            encrypted_username = self.encrypt(username)
            encrypted_password = self.encrypt(password)
            
            if not encrypted_username or not encrypted_password:
                return None
                
            # Create integrity hash
            integrity_data = f"{username}{password}"
            integrity_hash = hmac.new(
                self.cipher._signing_key,
                integrity_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return {
                'username': encrypted_username,
                'password': encrypted_password,
                'integrity_hash': integrity_hash
            }
            
        except Exception as e:
            self.logger.error(f"Credential encryption failed: {e}")
            return None
            
    def decrypt_credentials(self, encrypted_data: Dict) -> Optional[tuple]:
        """Decrypt credentials with integrity verification"""
        try:
            username = self.decrypt(encrypted_data['username'])
            password = self.decrypt(encrypted_data['password'])
            
            if not username or not password:
                return None
                
            # Verify integrity
            integrity_data = f"{username}{password}"
            expected_hash = hmac.new(
                self.cipher._signing_key,
                integrity_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_hash, encrypted_data['integrity_hash']):
                self.logger.error("Credential integrity check failed")
                return None
                
            return username, password
            
        except Exception as e:
            self.logger.error(f"Credential decryption failed: {e}")
            return None
            
    def secure_delete(self, filepath: str):
        """Securely delete file by overwriting with random data"""
        try:
            if os.path.exists(filepath):
                # Get file size
                file_size = os.path.getsize(filepath)
                
                # Overwrite with random data 3 times
                with open(filepath, 'wb') as f:
                    for _ in range(3):
                        f.write(os.urandom(file_size))
                        f.flush()
                        os.fsync(f.fileno())
                
                # Delete file
                os.remove(filepath)
                self.logger.info(f"File securely deleted: {filepath}")
                
        except Exception as e:
            self.logger.error(f"Secure delete failed: {e}")
            
    def generate_secure_hash(self, data: str, salt: str = None) -> str:
        """Generate secure hash for data"""
        if not salt:
            salt = os.urandom(16).hex()
            
        return hashlib.pbkdf2_hmac(
            'sha256',
            data.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        ).hex()