from app.middleware.permissions import require_permission
from astra_common.errors import AppError
from astra_common.security import create_jwt
from app.config import settings


class RequestState:
    user: dict


class FakeRequest:
    state = RequestState()


def test_admin_permission_allows():
    request = FakeRequest()
    request.state.user = {"permissions": ["*"]}
    require_permission(request, "strategy:create")


def test_missing_permission_rejected():
    request = FakeRequest()
    request.state.user = {"permissions": ["strategy:read"]}
    try:
        require_permission(request, "strategy:create")
    except AppError as exc:
        assert exc.code == "FORBIDDEN"
    else:
        raise AssertionError("permission should be rejected")


def test_market_data_permission_allows():
    request = FakeRequest()
    request.state.user = {"permissions": ["market_data:read"]}
    require_permission(request, "market_data:read")


def test_strategy_update_permission_allows_archive_and_update():
    request = FakeRequest()
    request.state.user = {"permissions": ["strategy:update"]}
    require_permission(request, "strategy:update")


def test_admin_wildcard_permission_allows_auth_me_proxy():
    request = FakeRequest()
    request.state.user = {"permissions": ["*"]}
    require_permission(request, "auth:me")


def test_lifecycle_read_permission_allows():
    request = FakeRequest()
    request.state.user = {"permissions": ["lifecycle:read"]}
    require_permission(request, "lifecycle:read")


def test_lifecycle_manage_permission_rejected_for_read_only():
    request = FakeRequest()
    request.state.user = {"permissions": ["lifecycle:read"]}
    try:
        require_permission(request, "lifecycle:manage")
    except AppError as exc:
        assert exc.code == "FORBIDDEN"
    else:
        raise AssertionError("lifecycle manage should require explicit permission")


def test_access_token_includes_jti_for_blacklist():
    token = create_jwt("u001", settings.jwt_secret, 60, {"token_type": "access", "jti": "jwt-id", "permissions": ["*"]})
    from astra_common.security import decode_jwt

    payload = decode_jwt(token, settings.jwt_secret)
    assert payload["jti"] == "jwt-id"
