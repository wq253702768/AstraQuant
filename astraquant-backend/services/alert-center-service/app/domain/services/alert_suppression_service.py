class AlertSuppressionService:
    def suppressed(self, event: dict) -> bool: return bool(event.get("suppressed"))
