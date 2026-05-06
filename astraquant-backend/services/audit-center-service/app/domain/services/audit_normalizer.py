class AuditNormalizer:
    def normalize(self, event: dict) -> dict: return {"level": event.get("level","NORMAL"), **event}
