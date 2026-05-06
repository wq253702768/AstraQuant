from decimal import Decimal
from uuid import uuid4
from app.domain.entities.drawdown import Drawdown

class DrawdownEngine:
    def calculate(self, equity_curve: list) -> tuple[Decimal, Decimal, list[Drawdown]]:
        if not equity_curve:
            return Decimal("0"), Decimal("0"), []
        peak = equity_curve[0].equity
        peak_time = equity_curve[0].ts
        max_dd = Decimal("0")
        max_amount = Decimal("0")
        trough_point = equity_curve[0]
        for point in equity_curve:
            if point.equity > peak:
                peak = point.equity; peak_time = point.ts
            dd = (point.equity - peak) / peak if peak else Decimal("0")
            if dd < max_dd:
                max_dd = dd
                max_amount = point.equity - peak
                trough_point = point
        drawdowns = []
        if max_dd < 0:
            drawdowns.append(Drawdown(drawdown_id=str(uuid4()), start_time=peak_time, trough_time=trough_point.ts, recovery_time=None, peak_equity=peak, trough_equity=trough_point.equity, drawdown_pct=max_dd, drawdown_amount=max_amount, status="active"))
        return max_dd, max_amount, drawdowns
