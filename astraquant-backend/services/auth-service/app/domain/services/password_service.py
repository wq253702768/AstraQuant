from astra_common.security import hash_password, verify_password

class PasswordService:
    def hash(self, password: str) -> str:
        return hash_password(password)
    def verify(self, password: str, password_hash: str) -> bool:
        return verify_password(password, password_hash)
