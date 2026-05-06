class EnableExchangeAccountService:
    async def execute(self, account_id: str, mode: str): return {"account_id": account_id, "status": "READ_ONLY", "trading_enabled": False}
