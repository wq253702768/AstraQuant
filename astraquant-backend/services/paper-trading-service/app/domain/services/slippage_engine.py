from decimal import Decimal
class SlippageEngine:
    def fill_price(self, side: str, action: str, bid: Decimal, ask: Decimal, slippage_pct: Decimal) -> tuple[Decimal, Decimal]:
        if side.upper() == "BUY":
            base = ask if action.upper() in {"OPEN", "CLOSE"} else ask
            return base * (Decimal("1") + slippage_pct), base * slippage_pct
        base = bid
        return base * (Decimal("1") - slippage_pct), base * slippage_pct
