PRIORITY = {
    "KLINE": 10,
    "SIGNAL": 20,
    "ORDER_CREATED": 30,
    "ORDER_FILLED": 40,
    "COST_CHARGED": 50,
    "FUNDING_FEE_CHARGED": 50,
    "POSITION_UPDATED": 60,
    "EQUITY_UPDATED": 70,
    "DRAWDOWN_UPDATED": 80,
    "RISK_TRIGGERED": 90,
}

class ReplayEventSorter:
    def sort(self, events: list) -> list:
        sorted_events = sorted(events, key=lambda event: (event.event_time, PRIORITY.get(event.event_type, 999), event.sequence_no))
        return [event.__class__(**{**event.__dict__, "sequence_no": index + 1}) for index, event in enumerate(sorted_events)]
