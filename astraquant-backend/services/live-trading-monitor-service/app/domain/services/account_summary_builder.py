from decimal import Decimal
class AccountSummaryBuilder:
    def build(self, start: Decimal, end: Decimal, orders: list[dict], trades: list[dict]) -> dict:
        return {"starting_equity": start, "ending_equity": end, "daily_return": (end-start)/start if start else Decimal("0"), "order_count": len(orders), "filled_order_count": sum(1 for o in orders if o.get("status") == "FILLED"), "failed_order_count": sum(1 for o in orders if o.get("status") == "FAILED"), "trade_count": len(trades), "fee_total": sum((Decimal(str(t.get("fee",0))) for t in trades), Decimal("0"))}
