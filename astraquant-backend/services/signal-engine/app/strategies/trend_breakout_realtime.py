from app.domain.services.signal_reason_builder import SignalReasonBuilder
from app.indicators.breakout import BreakoutIndicator
from app.indicators.volume import VolumeIndicator
from app.strategies.base import RealtimeStrategy

class TrendBreakoutRealtime(RealtimeStrategy):
    def generate(self, snapshot: dict, params: dict) -> list[dict]:
        kline = snapshot.get("kline") or {}
        if not kline.get("confirmed", True): return []
        klines = snapshot.get("klines") or [kline]
        window = int(params.get("breakout_window", 3))
        breakout = BreakoutIndicator().snapshot(klines, window)
        volume = VolumeIndicator().snapshot(klines, min(20, max(1, len(klines)-1)))
        signal = None
        if breakout["breakout_long"]: signal = {"signal_type":"OPEN_LONG","side":"BUY","position_side":"LONG","action":"OPEN"}
        elif breakout["breakout_short"]: signal = {"signal_type":"OPEN_SHORT","side":"SELL","position_side":"SHORT","action":"OPEN"}
        if not signal: return []
        signal.update({"reference_price": breakout["current_close"], "leverage": params.get("max_leverage", 1), "suggested_position_pct": params.get("risk_per_trade_pct", 0.005), "indicator_snapshot": {**breakout, **volume}, "reason": SignalReasonBuilder().trend_breakout(kline.get("timeframe","5m"), window), "bar_id": breakout.get("bar_id")})
        return [signal]
