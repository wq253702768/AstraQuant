from decimal import Decimal

class MetricsEngine:
    def calculate(self, initial_capital: Decimal, final_equity: Decimal, trades: list, max_drawdown: Decimal, max_drawdown_amount: Decimal) -> dict:
        net_profit = final_equity - initial_capital
        wins = [trade.realized_pnl for trade in trades if trade.realized_pnl > 0]
        losses = [trade.realized_pnl for trade in trades if trade.realized_pnl < 0]
        gross_profit = sum(wins, Decimal("0"))
        gross_loss = abs(sum(losses, Decimal("0")))
        trade_count = len(trades)
        return {
            "total_return": net_profit / initial_capital if initial_capital else Decimal("0"),
            "annual_return": Decimal("0"),
            "final_equity": final_equity,
            "max_drawdown": max_drawdown,
            "max_drawdown_amount": max_drawdown_amount,
            "win_rate": Decimal(len(wins)) / Decimal(trade_count) if trade_count else Decimal("0"),
            "profit_loss_ratio": (gross_profit / Decimal(len(wins))) / (gross_loss / Decimal(len(losses))) if wins and losses and gross_loss else Decimal("0"),
            "profit_factor": gross_profit / gross_loss if gross_loss else Decimal("0"),
            "trade_count": trade_count,
            "win_trade_count": len(wins),
            "loss_trade_count": len(losses),
            "max_consecutive_losses": self._max_consecutive_losses(trades),
            "avg_profit": gross_profit / Decimal(len(wins)) if wins else Decimal("0"),
            "avg_loss": gross_loss / Decimal(len(losses)) if losses else Decimal("0"),
            "fee_total": sum((trade.fee for trade in trades), Decimal("0")),
            "slippage_total": sum((abs(trade.slippage) for trade in trades), Decimal("0")),
            "funding_fee_total": sum((trade.funding_fee for trade in trades), Decimal("0")),
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "net_profit": net_profit,
            "decision": "BACKTEST_COMPLETED",
        }
    def _max_consecutive_losses(self, trades: list) -> int:
        max_losses = current = 0
        for trade in trades:
            if trade.realized_pnl < 0:
                current += 1
                max_losses = max(max_losses, current)
            else:
                current = 0
        return max_losses
