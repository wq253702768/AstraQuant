class AuditTraceBuilder:
    def key(self, event: dict) -> str: return event.get("trace_id") or event.get("metadata",{}).get("signal_id") or event.get("resource_id")
