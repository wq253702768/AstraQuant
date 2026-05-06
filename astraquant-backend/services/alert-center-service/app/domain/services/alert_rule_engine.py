class AlertRuleEngine:
    def match(self, event: dict) -> dict: return {"level": event.get("level", "INFO"), "enabled": True}
