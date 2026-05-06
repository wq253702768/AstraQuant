from astra_common.security import create_jwt, decode_jwt, hash_password, verify_password
from app.domain.services.token_service import TokenService


def test_password_hash():
    hashed = hash_password("password")
    assert hashed != "password"
    assert verify_password("password", hashed)


def test_jwt_roundtrip():
    token = create_jwt("u001", "secret", 60, {"roles": ["admin"]})
    payload = decode_jwt(token, "secret")
    assert payload["sub"] == "u001"
    assert payload["roles"] == ["admin"]


def test_token_service_access_token_claims():
    token = TokenService().create_access_token("u001", ["admin"], ["*"])
    payload = TokenService().decode(token)
    assert payload["sub"] == "u001"
    assert payload["token_type"] == "access"
    assert payload["roles"] == ["admin"]
    assert payload["permissions"] == ["*"]


def test_token_service_refresh_token_claims():
    token = TokenService().create_refresh_token("u001")
    payload = TokenService().decode(token)
    assert payload["sub"] == "u001"
    assert payload["token_type"] == "refresh"
