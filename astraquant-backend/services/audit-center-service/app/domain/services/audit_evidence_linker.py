class AuditEvidenceLinker:
    def link(self, event: dict) -> dict: return {"resource_type": event.get("resource_type"), "resource_id": event.get("resource_id")}
