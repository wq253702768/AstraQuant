from astra_common.errors import AppError
class PermissionValidator:
    def validate(self, scopes: list[str]) -> dict:
        normalized = {scope.upper() for scope in scopes}
        if "WITHDRAW" in normalized:
            raise AppError("CREDENTIAL_HAS_WITHDRAW_PERMISSION", "禁止保存带提现权限的 API Key", 400)
        return {"has_read_permission": "READ" in normalized, "has_trade_permission": "TRADE" in normalized, "has_withdraw_permission": False, "permission_scopes": sorted(normalized)}
