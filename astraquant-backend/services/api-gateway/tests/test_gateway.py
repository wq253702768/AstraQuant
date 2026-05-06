from astra_common.security import create_jwt, decode_jwt


def test_gateway_token_claims():
    token = create_jwt("u001", "change_me", 60, {"roles": ["admin"], "permissions": ["*"]})
    payload = decode_jwt(token, "change_me")
    assert payload["sub"] == "u001"
    assert payload["permissions"] == ["*"]
