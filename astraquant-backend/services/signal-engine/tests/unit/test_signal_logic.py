from app.domain.services.signal_cooldown_service import SignalCooldownService
from app.domain.services.signal_dedup_service import SignalDedupService
from app.domain.services.signal_payload_builder import SignalPayloadBuilder
from app.domain.services.signal_precheck_service import SignalPrecheckService
from app.indicators.breakout import BreakoutIndicator
from app.strategies.trend_breakout_realtime import TrendBreakoutRealtime


def snapshot(close="110", high1="105", low1="95", fresh=True, spread="0.0001", funding="0.0001"):
    return {"fresh": fresh, "freshness": {"fresh": fresh, "freshness_status": "FRESH" if fresh else "STALE"}, "bbo": {"bid_price":"100","ask_price":"101","spread_pct": spread}, "funding": {"funding_rate": funding}, "market": {"last_price": close}, "mark_price": {"mark_price": close}, "kline": {"timeframe":"5m","confirmed": True,"bar_id":"bar1","open":"100","high":close,"low":"99","close":close,"volume":"200"}, "klines": [{"high": high1, "low": low1, "close":"100", "volume":"100"}, {"timeframe":"5m","confirmed": True,"bar_id":"bar1","open":"100","high":close,"low":"99","close":close,"volume":"200"}]}

def test_trend_breakout_open_long():
    signals = TrendBreakoutRealtime().generate(snapshot(), {"breakout_window": 1, "max_leverage": 3, "risk_per_trade_pct": 0.005})
    assert signals[0]["signal_type"] == "OPEN_LONG"

def test_trend_breakout_open_short():
    s = snapshot(close="90", high1="105", low1="95")
    s["kline"]["low"] = "90"; s["klines"][-1]["low"] = "90"
    signals = TrendBreakoutRealtime().generate(s, {"breakout_window": 1})
    assert signals[0]["signal_type"] == "OPEN_SHORT"

def test_precheck_reject_stale_data(): assert not SignalPrecheckService().check(snapshot(fresh=False), {}, True).allowed

def test_precheck_reject_high_spread(): assert not SignalPrecheckService().check(snapshot(spread="0.01"), {}, True).allowed

def test_precheck_reject_high_funding(): assert not SignalPrecheckService().check(snapshot(funding="0.01"), {}, True).allowed

def test_signal_dedup_same_bar():
    d = SignalDedupService(); assert d.allow_bar("s","BTC","bar1","OPEN_LONG"); assert not d.allow_bar("s","BTC","bar1","OPEN_LONG")

def test_signal_cooldown():
    c = SignalCooldownService(); assert c.allow("k", 60); assert not c.allow("k", 60)

def test_indicator_breakout_window(): assert BreakoutIndicator().snapshot(snapshot()["klines"], 1)["breakout_long"] is True

def test_signal_payload_builder(): assert SignalPayloadBuilder().market_snapshot(snapshot())["last_price"] == "110"

def test_signal_reason_builder(): assert "突破" in TrendBreakoutRealtime().generate(snapshot(), {"breakout_window": 1})[0]["reason"]
