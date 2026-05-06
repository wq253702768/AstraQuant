class DisableExchangeAccountService:
    async def execute(self, account_id: str, reason: str): return {"account_id": account_id, "status": "DISABLED"}
