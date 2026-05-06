from decimal import Decimal
from app.domain.services.account_engine import AccountEngine
from app.domain.services.fee_engine import FeeEngine
from app.domain.services.funding_engine import FundingEngine
from app.domain.services.ledger_engine import LedgerEngine
from app.domain.services.matching_engine import MatchingEngine
from app.domain.services.order_engine import OrderEngine
from app.domain.services.pnl_engine import PnLEngine
from app.domain.services.position_engine import PositionEngine
from app.domain.services.slippage_engine import SlippageEngine


def risk(side="BUY", action="OPEN", position_side="LONG"):
    return {"risk_decision_id":"00000000-0000-0000-0000-000000000001","signal_id":"00000000-0000-0000-0000-000000000002","strategy_id":"00000000-0000-0000-0000-000000000003","strategy_version_id":"00000000-0000-0000-0000-000000000004","internal_symbol":"BTC-USDT-SWAP","side":side,"position_side":position_side,"action":action,"reference_price":"100","quantity":"1","leverage":"2"}


def test_create_paper_account():
    account = AccountEngine().create("demo", "OKX", "USDT", Decimal("10000"))
    assert account.equity == Decimal("10000")


def test_market_order_long_fill_price():
    order = OrderEngine().create_market_order(risk(), "acc")
    fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"})
    assert fill["fill_price"] > Decimal("100")


def test_market_order_short_fill_price():
    order = OrderEngine().create_market_order(risk("SELL", "OPEN", "SHORT"), "acc")
    fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"})
    assert fill["fill_price"] < Decimal("99")


def test_fee_calculation(): assert FeeEngine().fee(Decimal("1000"), Decimal("0.0005")) == Decimal("0.5000")

def test_slippage_calculation(): assert SlippageEngine().fill_price("BUY", "OPEN", Decimal("99"), Decimal("100"), Decimal("0.001"))[0] == Decimal("100.100")

def test_open_long_position():
    order = OrderEngine().create_market_order(risk(), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); assert pos.quantity == Decimal("1")

def test_close_long_position():
    order = OrderEngine().create_market_order(risk(), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); pnl = PositionEngine().close_long(pos, Decimal("1"), Decimal("110")); assert pnl > 0

def test_open_short_position():
    order = OrderEngine().create_market_order(risk("SELL", "OPEN", "SHORT"), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); assert pos.position_side == "SHORT"

def test_close_short_position():
    order = OrderEngine().create_market_order(risk("SELL", "OPEN", "SHORT"), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); pnl = PositionEngine().close_short(pos, Decimal("1"), Decimal("90")); assert pnl > 0

def test_position_average_price():
    order = OrderEngine().create_market_order(risk(), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); PositionEngine().add(pos, Decimal("1"), Decimal("120")); assert pos.quantity == Decimal("2")

def test_unrealized_pnl_long():
    order = OrderEngine().create_market_order(risk(), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); assert PnLEngine().unrealized(pos, Decimal("110")) > 0

def test_unrealized_pnl_short():
    order = OrderEngine().create_market_order(risk("SELL", "OPEN", "SHORT"), "acc"); fill = MatchingEngine().fill(order, {"bid_price":"99", "ask_price":"100"}); pos = PositionEngine().open_position("acc", order, fill); assert PnLEngine().unrealized(pos, Decimal("90")) > 0

def test_funding_fee_pay(): assert FundingEngine().funding_fee(Decimal("1000"), Decimal("0.0001"), "LONG") == Decimal("0.1000")

def test_funding_fee_receive(): assert FundingEngine().funding_fee(Decimal("1000"), Decimal("0.0001"), "SHORT") == Decimal("-0.1000")

def test_order_idempotency(): assert "paper_order:" in OrderEngine().create_market_order(risk(), "acc").idempotency_key

def test_ledger_entry(): assert LedgerEngine().entry("acc", "TRADE_FEE", Decimal("-1"), Decimal("100"), Decimal("99"), "fee").balance_after == Decimal("99")
