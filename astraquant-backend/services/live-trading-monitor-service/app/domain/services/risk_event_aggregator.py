class RiskEventAggregator:
    def aggregate(self, events: list[dict]) -> dict: return {"circuit_breaker_count": len([e for e in events if e.get("event_type") == "live_risk.breaker.triggered"]), "order_unknown_count": len([e for e in events if e.get("event_type") == "order.unknown"])}
