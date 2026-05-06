from datetime import UTC, datetime, timedelta

from app.domain.services.cursor_paginator import CursorPaginator
from app.domain.services.replay_cache_key_builder import ReplayCacheKeyBuilder
from app.domain.services.replay_event_builder import ReplayEventBuilder
from app.domain.services.replay_event_sorter import ReplayEventSorter
from app.domain.services.replay_marker_builder import ReplayMarkerBuilder
from app.domain.services.replay_window_planner import ReplayWindowPlanner


def trade(reason="突破", funding_fee="0", side="buy", action="open"):
    return {"task_id": "00000000-0000-0000-0000-000000000001", "drawdown_id": "00000000-0000-0000-0000-000000000002", "trade_time": datetime(2026, 1, 1, tzinfo=UTC), "exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "strategy_id": "00000000-0000-0000-0000-000000000003", "strategy_version_id": "00000000-0000-0000-0000-000000000004", "side": side, "position_side": "long", "action": action, "order_type": "IOC", "order_price": "100", "fill_price": "101", "size": "1", "leverage": "3", "fee": "1", "slippage": "0.1", "funding_fee": funding_fee, "realized_pnl": "0", "equity_after": "10000", "cl_ord_id": "BT_1", "reason": reason}


def drawdown():
    return {"drawdown_id": "00000000-0000-0000-0000-000000000002", "trough_time": datetime(2026, 1, 1, tzinfo=UTC)}


def test_build_order_filled_event():
    event = ReplayEventBuilder().build_order_filled_event(trade(), drawdown(), 1)
    assert event.event_type == "ORDER_FILLED"
    assert event.marker_type == "OPEN_LONG"


def test_build_stop_loss_event():
    event = ReplayEventBuilder().build_order_filled_event(trade("触发固定止损"), drawdown(), 1)
    assert event.event_type == "STOP_LOSS"


def test_build_take_profit_event():
    event = ReplayEventBuilder().build_order_filled_event(trade("达到2R止盈"), drawdown(), 1)
    assert event.event_type == "TAKE_PROFIT"


def test_build_funding_fee_event():
    event = ReplayEventBuilder().build_order_filled_event(trade(funding_fee="-0.98"), drawdown(), 1)
    assert event.event_type == "FUNDING_FEE_CHARGED"
    assert event.marker_type == "FUNDING_FEE"


def test_build_equity_and_drawdown_event():
    point = {"task_id": trade()["task_id"], "ts": datetime(2026, 1, 1, tzinfo=UTC), "exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "strategy_id": trade()["strategy_id"], "strategy_version_id": trade()["strategy_version_id"], "equity": "10000", "drawdown_pct": "0"}
    builder = ReplayEventBuilder()
    assert builder.build_equity_event(point, drawdown(), 1).event_type == "EQUITY_UPDATED"
    assert builder.build_drawdown_event(point, drawdown(), 2).event_type == "DRAWDOWN_UPDATED"


def test_replay_event_sorter():
    builder = ReplayEventBuilder()
    e1 = builder.build_equity_event({"task_id": trade()["task_id"], "ts": datetime(2026, 1, 1, 0, 1, tzinfo=UTC), "strategy_id": trade()["strategy_id"], "strategy_version_id": trade()["strategy_version_id"]}, drawdown(), 10)
    e2 = builder.build_order_filled_event(trade(), drawdown(), 1)
    sorted_events = ReplayEventSorter().sort([e1, e2])
    assert sorted_events[0].event_type == "ORDER_FILLED"
    assert sorted_events[0].sequence_no == 1


def test_replay_window_planner():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    windows = ReplayWindowPlanner().plan(start, start + timedelta(hours=3), 60)
    assert len(windows) == 3


def test_replay_cache_key():
    key = ReplayCacheKeyBuilder().events("dd", "a", "b")
    assert key.startswith("replay:events:dd:")


def test_cursor_pagination():
    page, cursor = CursorPaginator().page([1, 2, 3], 2)
    assert page == [1, 2]
    assert CursorPaginator().page([1, 2, 3], 2, cursor)[0] == [3]


def test_marker_builder_close_short():
    assert ReplayMarkerBuilder().from_trade(trade(side="buy", action="close")) == "CLOSE_SHORT"
