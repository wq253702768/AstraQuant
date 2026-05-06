from decimal import Decimal
from app.engine.signal_generator import TradeSignal
from app.strategies.base import Strategy

class TrendBreakoutStrategy(Strategy):
    def generate_signals(self, rows: list[dict], params: dict) -> list[TradeSignal]:
        window = int(params.get("breakout_window", 3))
        leverage = Decimal(str(params.get("max_leverage", 1)))
        risk_pct = Decimal(str(params.get("risk_per_trade_pct", "0.005")))
        signals: list[TradeSignal] = []
        for index in range(window, len(rows)):
            history = rows[index-window:index]
            current = rows[index]
            close = Decimal(str(current["close"]))
            high = max(Decimal(str(item["high"])) for item in history)
            low = min(Decimal(str(item["low"])) for item in history)
            symbol = current.get("internal_symbol") or current.get("symbol") or params.get("symbols", [""])[0]
            if close > high:
                signals.append(TradeSignal(signal_time=current["ts"], symbol=symbol, signal_type="OPEN_LONG", side="buy", position_side="long", action="open", price=close, size=risk_pct, leverage=leverage, reason="突破历史高点"))
                break
            if close < low:
                signals.append(TradeSignal(signal_time=current["ts"], symbol=symbol, signal_type="OPEN_SHORT", side="sell", position_side="short", action="open", price=close, size=risk_pct, leverage=leverage, reason="跌破历史低点"))
                break
        return signals
