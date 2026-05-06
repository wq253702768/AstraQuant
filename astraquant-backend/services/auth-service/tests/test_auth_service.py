from astra_common.security import create_jwt, decode_jwt, hash_password, verify_password


def test_password_hash():
    hashed = hash_password("password")
    assert hashed != "password"
    assert verify_password("password", hashed)


def test_jwt_roundtrip():
    token = create_jwt("u001", "secret", 60, {"roles": ["admin"]})
    payload = decode_jwt(token, "secret")
    assert payload["sub"] == "u001"
    assert payload["roles"] == ["admin"]
