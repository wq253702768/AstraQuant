from datetime import UTC, datetime, timedelta
from decimal import Decimal

from app.engine.cost_engine import CostEngine
from app.engine.data_validator import DataValidator
from app.engine.drawdown_engine import DrawdownEngine
from app.engine.equity_engine import EquityEngine
from app.engine.matching_engine import MatchingEngine
from app.engine.metrics_engine import MetricsEngine
from app.engine.order_simulator import OrderSimulator
from app.engine.position_engine import PositionEngine
from app.engine.risk_engine import RiskEngine
from app.engine.strategy_runner import StrategyRunner


def rows():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    return [
        {"ts": start, "internal_symbol": "BTC-USDT-SWAP", "open": Decimal("100"), "high": Decimal("105"), "low": Decimal("95"), "close": Decimal("100")},
        {"ts": start + timedelta(minutes=5), "internal_symbol": "BTC-USDT-SWAP", "open": Decimal("100"), "high": Decimal("106"), "low": Decimal("96"), "close": Decimal("101")},
        {"ts": start + timedelta(minutes=10), "internal_symbol": "BTC-USDT-SWAP", "open": Decimal("101"), "high": Decimal("110"), "low": Decimal("100"), "close": Decimal("108")},
    ]


def test_data_validator_pass():
    assert DataValidator().validate_klines(rows()).status == "PASS"


def test_data_validator_failed():
    assert DataValidator().validate_klines([]).status == "FAILED"


def test_trend_breakout_signal():
    signals = StrategyRunner().run("trend_breakout", rows(), {"breakout_window": 2, "symbols": ["BTC-USDT-SWAP"], "max_leverage": 3, "risk_per_trade_pct": "0.01"})
    assert signals and signals[0].signal_type == "OPEN_LONG"


def test_order_simulator_ioc():
    signal = StrategyRunner().run("trend_breakout", rows(), {"breakout_window": 2, "symbols": ["BTC-USDT-SWAP"], "max_leverage": 3, "risk_per_trade_pct": "0.01"})[0]
    order = OrderSimulator().create_order(signal, Decimal("10000"))
    assert order.order_type == "IOC"
    assert order.size > 0


def test_matching_engine_limit():
    signal = StrategyRunner().run("trend_breakout", rows(), {"breakout_window": 2, "symbols": ["BTC-USDT-SWAP"], "max_leverage": 3, "risk_per_trade_pct": "0.01"})[0]
    order = OrderSimulator().create_order(signal, Decimal("10000"))
    trade = MatchingEngine().match(order, rows()[-1], {"taker_fee_rate": "0.0005", "default_slippage": "0.0003"}, Decimal("10000"))
    assert trade is not None
    assert trade.fee > 0


def test_position_open_close():
    signal = StrategyRunner().run("trend_breakout", rows(), {"breakout_window": 2, "symbols": ["BTC-USDT-SWAP"], "max_leverage": 3, "risk_per_trade_pct": "0.01"})[0]
    order = OrderSimulator().create_order(signal, Decimal("10000"))
    trade = MatchingEngine().match(order, rows()[-1], {"taker_fee_rate": "0.0005", "default_slippage": "0.0003"}, Decimal("10000"))
    position = PositionEngine().apply_trade(None, trade)
    assert position.quantity > 0


def test_cost_engine_fee_slippage_funding():
    engine = CostEngine()
    assert engine.fee(Decimal("100"), Decimal("2"), Decimal("0.001")) == Decimal("0.200")
    fill, slip = engine.apply_slippage(Decimal("100"), "buy", Decimal("0.001"))
    assert fill == Decimal("100.100") and slip == Decimal("0.100")
    assert engine.funding_fee(Decimal("1000"), Decimal("0.0001")) == Decimal("0.1000")


def test_equity_engine():
    point = EquityEngine().point(datetime(2026, 1, 1, tzinfo=UTC), Decimal("10000"), Decimal("100"), Decimal("50"), Decimal("10"), Decimal("5"), Decimal("10000"))
    assert point.equity == Decimal("10135")


def test_drawdown_engine():
    t = datetime(2026, 1, 1, tzinfo=UTC)
    curve = [EquityEngine().point(t, Decimal("10000"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("10000")), EquityEngine().point(t + timedelta(minutes=5), Decimal("10000"), Decimal("-500"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("10000"))]
    max_dd, _, drawdowns = DrawdownEngine().calculate(curve)
    assert max_dd == Decimal("-0.05")
    assert drawdowns


def test_metrics_engine():
    metrics = MetricsEngine().calculate(Decimal("10000"), Decimal("11000"), [], Decimal("-0.1"), Decimal("-1000"))
    assert metrics["total_return"] == Decimal("0.1")
    assert metrics["net_profit"] == Decimal("1000")


def test_risk_engine():
    signal = StrategyRunner().run("trend_breakout", rows(), {"breakout_window": 2, "symbols": ["BTC-USDT-SWAP"], "max_leverage": 3, "risk_per_trade_pct": "0.01"})[0]
    assert RiskEngine().check(signal, {"max_leverage": 3}).decision == "APPROVE"
    assert RiskEngine().check(signal, {"max_leverage": 1}).decision == "REJECT"
