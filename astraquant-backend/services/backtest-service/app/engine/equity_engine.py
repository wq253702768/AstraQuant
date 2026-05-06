from decimal import Decimal
from app.domain.entities.equity_point import EquityPoint

class EquityEngine:
    def point(self, ts, initial_capital: Decimal, realized_pnl: Decimal, unrealized_pnl: Decimal, fee_total: Decimal, funding_fee_total: Decimal, peak_equity: Decimal) -> EquityPoint:
        equity = initial_capital + realized_pnl + unrealized_pnl - fee_total - funding_fee_total
        drawdown = Decimal("0") if peak_equity <= 0 else (equity - peak_equity) / peak_equity
        return EquityPoint(ts=ts, equity=equity, cash=initial_capital + realized_pnl - fee_total - funding_fee_total, position_value=Decimal("0"), realized_pnl=realized_pnl, unrealized_pnl=unrealized_pnl, fee_total=fee_total, funding_fee_total=funding_fee_total, drawdown_pct=drawdown)
