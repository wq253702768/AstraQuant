from decimal import Decimal
class BreakoutIndicator:
    def snapshot(self, klines: list[dict], window: int) -> dict:
        history = klines[-window-1:-1] if len(klines) > window else klines[:-1]
        current = klines[-1]
        highest = max(Decimal(str(item["high"])) for item in history) if history else Decimal(str(current["high"]))
        lowest = min(Decimal(str(item["low"])) for item in history) if history else Decimal(str(current["low"]))
        close = Decimal(str(current["close"]))
        return {"breakout_window": window, "highest_high": str(highest), "lowest_low": str(lowest), "current_close": str(close), "breakout_long": close > highest, "breakout_short": close < lowest, "bar_id": current.get("bar_id")}
