from app.domain.entities.replay_event import ReplayEvent
from app.domain.services.replay_marker_builder import ReplayMarkerBuilder

class ReplayEventBuilder:
    def build_order_filled_event(self, trade: dict, drawdown: dict, sequence_no: int) -> ReplayEvent:
        marker = ReplayMarkerBuilder().from_trade(trade)
        event_type = "ORDER_FILLED"
        if marker in {"STOP_LOSS", "TAKE_PROFIT", "FUNDING_FEE"}:
            event_type = "FUNDING_FEE_CHARGED" if marker == "FUNDING_FEE" else marker
        return ReplayEvent(
            task_id=trade["task_id"],
            drawdown_id=drawdown["drawdown_id"],
            event_time=trade["trade_time"],
            event_type=event_type,
            marker_type=marker or None,
            exchange=trade.get("exchange", "OKX"),
            internal_symbol=trade["internal_symbol"],
            strategy_id=trade["strategy_id"],
            strategy_version_id=trade["strategy_version_id"],
            sequence_no=sequence_no,
            payload={k: v for k, v in trade.items() if k not in {"task_id", "strategy_id", "strategy_version_id"}},
        )

    def build_equity_event(self, point: dict, drawdown: dict, sequence_no: int) -> ReplayEvent:
        return ReplayEvent(task_id=point["task_id"], drawdown_id=drawdown["drawdown_id"], event_time=point["ts"], event_type="EQUITY_UPDATED", marker_type=None, exchange=point.get("exchange", "OKX"), internal_symbol=point.get("internal_symbol", ""), strategy_id=point["strategy_id"], strategy_version_id=point["strategy_version_id"], sequence_no=sequence_no, payload=point)

    def build_drawdown_event(self, point: dict, drawdown: dict, sequence_no: int) -> ReplayEvent:
        payload = dict(point)
        payload["is_trough"] = point.get("ts") == drawdown.get("trough_time")
        return ReplayEvent(task_id=point["task_id"], drawdown_id=drawdown["drawdown_id"], event_time=point["ts"], event_type="DRAWDOWN_UPDATED", marker_type=None, exchange=point.get("exchange", "OKX"), internal_symbol=point.get("internal_symbol", ""), strategy_id=point["strategy_id"], strategy_version_id=point["strategy_version_id"], sequence_no=sequence_no, payload=payload)

    def build(self, drawdown: dict, trades: list[dict], equity_curve: list[dict]) -> list[ReplayEvent]:
        events: list[ReplayEvent] = []
        seq = 1
        for trade in trades:
            events.append(self.build_order_filled_event(trade, drawdown, seq)); seq += 1
        for point in equity_curve:
            events.append(self.build_equity_event(point, drawdown, seq)); seq += 1
            events.append(self.build_drawdown_event(point, drawdown, seq)); seq += 1
        return events
