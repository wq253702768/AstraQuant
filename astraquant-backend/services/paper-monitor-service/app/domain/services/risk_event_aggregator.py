class RiskEventAggregator:
    def aggregate(self, events: list[dict]) -> dict:
        return {"risk_reject_count": sum(1 for e in events if e.get("decision") == "REJECT"), "pause_strategy_count": sum(1 for e in events if e.get("decision") == "PAUSE_STRATEGY"), "data_stale_count": sum(1 for e in events if "STALE" in str(e))}
