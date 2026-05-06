class QueryLiveDashboardService:
    async def execute(self): return {"account":{},"orders":{},"positions":{},"risk":{"risk_state":"NORMAL"},"observation":{"status":"RUNNING","latest_decision":"CONTINUE_SMALL_LIVE"}}
