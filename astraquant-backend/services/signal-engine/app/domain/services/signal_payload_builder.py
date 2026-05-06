class SignalPayloadBuilder:
    def market_snapshot(self, snapshot: dict) -> dict:
        market=snapshot.get("market") or {}; bbo=snapshot.get("bbo") or {}; mark=snapshot.get("mark_price") or {}; funding=snapshot.get("funding") or {}
        return {"last_price": market.get("last_price"), "bid_price": bbo.get("bid_price"), "ask_price": bbo.get("ask_price"), "mark_price": mark.get("mark_price"), "funding_rate": funding.get("funding_rate")}
