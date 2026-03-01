"""
Keychain/Secrets Manager utilities for backend development.

In production, use AWS Secrets Manager, HashiCorp Vault, or similar.
"""

import os
import json
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet


class LocalSecretsManager:
    """
    Local development secrets manager.

    In production, replace with AWS Secrets Manager or similar.
    """

    def __init__(self, secrets_file: Optional[str] = None):
        if secrets_file is None:
            # Check for secrets file in various locations
            possible_locations = [
                "secrets.env",
                ".env.local",
                ".env",
                os.path.expanduser("~/.kenkoumon/secrets.env"),
            ]
            for location in possible_locations:
                if os.path.exists(location):
                    secrets_file = location
                    break

        self.secrets_file = secrets_file
        self._secrets = {}
        if secrets_file and os.path.exists(secrets_file):
            self._load_secrets()

    def _load_secrets(self):
        """Load secrets from file."""
        with open(self.secrets_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    self._secrets[key.strip()] = value.strip()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value."""
        # Check secrets file first
        if key in self._secrets:
            return self._secrets[key]

        # Check environment variable
        value = os.environ.get(key)
        if value:
            return value

        return default

    def set(self, key: str, value: str):
        """Set a secret value (in memory only)."""
        self._secrets[key] = value

    def require(self, key: str) -> str:
        """Get a required secret, raise error if missing."""
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required secret '{key}' is not set")
        return value


class EncryptionService:
    """
    AES-256 encryption for sensitive data at rest.
    """

    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption service.

        Args:
            encryption_key: Base64-encoded Fernet key.
                          If not provided, reads from ENCRYPTION_KEY env var.
        """
        key = encryption_key or os.environ.get("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable is required")

        self.cipher = Fernet(key.encode() if isinstance(key, str) else key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data."""
        return self.cipher.encrypt(data)

    def encrypt_string(self, text: str) -> str:
        """Encrypt string and return base64-encoded ciphertext."""
        return self.encrypt(text.encode()).decode()

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypt data."""
        return self.cipher.decrypt(ciphertext)

    def decrypt_string(self, ciphertext: str) -> str:
        """Decrypt base64-encoded ciphertext."""
        return self.decrypt(ciphertext.encode()).decode()


# Singleton instance
_secrets_manager = None


def get_secrets_manager() -> LocalSecretsManager:
    """Get the secrets manager singleton."""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = LocalSecretsManager()
    return _secrets_manager


def get_encryption_service() -> EncryptionService:
    """Get the encryption service singleton."""
    return EncryptionService()


# Convenience functions
def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a secret value."""
    return get_secrets_manager().get(key, default)


def require_secret(key: str) -> str:
    """Get a required secret, raise error if missing."""
    return get_secrets_manager().require(key)


def encrypt_for_storage(text: str) -> str:
    """Encrypt text for storage in database."""
    return get_encryption_service().encrypt_string(text)


def decrypt_from_storage(ciphertext: str) -> str:
    """Decrypt text from database."""
    return get_encryption_service().decrypt_string(ciphertext)
