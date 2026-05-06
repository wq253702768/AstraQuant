class BacktestServiceClient:
    async def summary(self, backtest_task_id: str) -> dict:
        return {"task_id": backtest_task_id, "strategy_id": "00000000-0000-0000-0000-000000000001", "strategy_version_id": "00000000-0000-0000-0000-000000000002", "total_return": 0.128, "annual_return": 0.36, "final_equity": 11280, "max_drawdown": -0.056, "win_rate": 0.482, "profit_loss_ratio": 1.62, "profit_factor": 1.38, "trade_count": 126, "max_consecutive_losses": 4, "fee_total": 126.4, "slippage_total": 72.8, "funding_fee_total": -18.2, "net_profit": 1280, "max_leverage": 3}
