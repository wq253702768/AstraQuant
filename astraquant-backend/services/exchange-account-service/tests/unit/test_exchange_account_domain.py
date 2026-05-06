import pytest
from astra_common.errors import AppError
from app.domain.services.account_state_projection import AccountStateProjection
from app.domain.services.audit_log_service import AuditLogService
from app.domain.services.credential_encrypt_service import CredentialEncryptService
from app.domain.services.credential_mask_service import CredentialMaskService
from app.domain.services.permission_validator import PermissionValidator


def test_credential_mask(): assert CredentialMaskService().mask("abcd1234wxyz") == "abcd****wxyz"

def test_credential_decrypt():
    service = CredentialEncryptService(); encrypted = service.encrypt("secret"); assert service.decrypt(encrypted) == "secret"

def test_bind_credential_encrypt(): assert CredentialEncryptService().encrypt("api") != "api"

def test_reject_withdraw_permission():
    with pytest.raises(AppError): PermissionValidator().validate(["READ", "WITHDRAW"])

def test_permission_validator_read_only():
    result = PermissionValidator().validate(["READ"]); assert result["has_read_permission"] and not result["has_trade_permission"]

def test_account_status_transition():
    from app.domain.services.account_status_service import AccountStatusService
    assert AccountStatusService().enabled_status(False) == ("READ_ONLY", False)

def test_account_state_projection(): assert AccountStateProjection().project_account({"a": 1}) == {"a": 1}

def test_position_state_projection(): assert AccountStateProjection().project_position({"p": 1}) == {"p": 1}

def test_order_state_projection(): assert AccountStateProjection().project_order({"o": 1}) == {"o": 1}

def test_audit_log_created(): assert AuditLogService().build("BIND", "SUCCESS")["action"] == "BIND"
