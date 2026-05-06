from decimal import Decimal
class EquityCurveBuilder:
    def point(self, event: dict) -> dict:
        total = Decimal(str(event.get("total_equity", "0")))
        start = Decimal(str(event.get("starting_equity", total or 1)))
        return {"total_equity": total, "drawdown_pct": (total-start)/start if start else Decimal("0")}
