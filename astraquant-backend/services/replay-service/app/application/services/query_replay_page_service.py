class QueryReplayPageService:
    async def execute(self, drawdown_id: str):
        return {"drawdown": {"drawdown_id": drawdown_id}, "summary": {"trade_count": 0, "win_rate": "0", "fee_total": "0", "slippage_total": "0", "funding_fee_total": "0", "main_cause": "待分析"}, "available_event_types": ["ORDER_FILLED", "STOP_LOSS", "TAKE_PROFIT", "EQUITY_UPDATED", "DRAWDOWN_UPDATED"]}
