class AuditLogService:
    def build(self, action: str, result: str, message: str | None = None) -> dict: return {"action": action, "result": result, "message": message}
