from pydantic import BaseModel
class BindCredentialRequest(BaseModel):
    api_key: str
    secret_key: str
    passphrase: str | None = None
    permission_scopes: list[str]
class CredentialResponse(BaseModel):
    credential_id: str
    api_key_masked: str
    status: str
    has_read_permission: bool
    has_trade_permission: bool
    has_withdraw_permission: bool
