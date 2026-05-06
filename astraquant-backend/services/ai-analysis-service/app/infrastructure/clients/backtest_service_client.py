class BacktestServiceClient:
    async def load_review_input(self, backtest_task_id: str) -> dict:
        return {"backtest_result": {"task_id": backtest_task_id, "total_return": 0.128, "max_drawdown": -0.056, "win_rate": 0.482, "profit_factor": 1.38, "trade_count": 126, "fee_total": 126.4, "slippage_total": 72.8, "funding_fee_total": -18.2, "net_profit": 1280}, "drawdowns": [{"drawdown_id": "dd_mock", "trade_count": 14, "win_rate": 0.285}], "trade_summary": {"max_consecutive_losses": 4}, "cost_summary": {"cost_to_profit_ratio": 0.17}, "sample_trades": []}
