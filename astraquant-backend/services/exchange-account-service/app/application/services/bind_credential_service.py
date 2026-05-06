from app.domain.services.credential_encrypt_service import CredentialEncryptService
from app.domain.services.credential_mask_service import CredentialMaskService
from app.domain.services.permission_validator import PermissionValidator
from app.infrastructure.postgres.models import ExchangeAPICredentialModel
from app.infrastructure.repositories.credential_repository import CredentialRepository
from app.schemas.credential import BindCredentialRequest, CredentialResponse
class BindCredentialService:
    def __init__(self, session): self.repo=CredentialRepository(session); self.crypto=CredentialEncryptService(); self.mask=CredentialMaskService(); self.validator=PermissionValidator()
    async def execute(self, account_id: str, payload: BindCredentialRequest, operator_id: str|None):
        permissions=self.validator.validate(payload.permission_scopes)
        model=await self.repo.create(ExchangeAPICredentialModel(account_id=account_id,exchange="OKX",api_key_masked=self.mask.mask(payload.api_key),api_key_hash=self.crypto.hash_api_key(payload.api_key),encrypted_api_key=self.crypto.encrypt(payload.api_key),encrypted_secret_key=self.crypto.encrypt(payload.secret_key),encrypted_passphrase=self.crypto.encrypt(payload.passphrase) if payload.passphrase else None,encrypted_data_key="local",key_provider="LOCAL",algorithm="FERNET",status="ENCRYPTED",created_by=operator_id,**permissions))
        return CredentialResponse(credential_id=model.id,api_key_masked=model.api_key_masked,status=model.status,has_read_permission=model.has_read_permission,has_trade_permission=model.has_trade_permission,has_withdraw_permission=model.has_withdraw_permission)
