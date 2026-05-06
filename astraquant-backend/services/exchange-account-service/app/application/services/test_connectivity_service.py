class TestConnectivityService:
    async def execute(self, account_id: str): return {"account_id": account_id, "status": "SUCCESS", "read_permission": True, "trade_permission": False, "withdraw_permission": False, "ip_whitelist_status": "PASS", "account_config_readable": True}
