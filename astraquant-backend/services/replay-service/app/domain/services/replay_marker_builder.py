class ReplayMarkerBuilder:
    def from_trade(self, trade: dict) -> str:
        action = str(trade.get("action", "")).lower()
        side = str(trade.get("side", "")).lower()
        reason = str(trade.get("reason", "")).lower()
        funding_fee = str(trade.get("funding_fee", "0"))
        if funding_fee not in {"", "0", "0.0", "0.0000000000000000"}:
            return "FUNDING_FEE"
        if "stop" in reason or "止损" in reason:
            return "STOP_LOSS"
        if "profit" in reason or "止盈" in reason:
            return "TAKE_PROFIT"
        if action == "open" and side == "buy":
            return "OPEN_LONG"
        if action == "open" and side == "sell":
            return "OPEN_SHORT"
        if action in {"close", "reduce"} and side == "sell":
            return "CLOSE_LONG"
        if action in {"close", "reduce"} and side == "buy":
            return "CLOSE_SHORT"
        return ""
