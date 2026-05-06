class AlertEscalationService:
    def escalate(self, level: str, occurrence_count: int) -> str:
        if level == "WARNING" and occurrence_count > 5: return "CRITICAL"
        if level == "CRITICAL" and occurrence_count > 5: return "FATAL"
        return level
