import base64, hashlib
from cryptography.fernet import Fernet
from app.config import settings
class CredentialEncryptService:
    def _fernet(self):
        key = base64.urlsafe_b64encode(hashlib.sha256(settings.local_master_key.encode()).digest())
        return Fernet(key)
    def encrypt(self, value: str) -> str: return self._fernet().encrypt(value.encode()).decode()
    def decrypt(self, value: str) -> str: return self._fernet().decrypt(value.encode()).decode()
    def hash_api_key(self, api_key: str) -> str: return hashlib.sha256(api_key.encode()).hexdigest()
