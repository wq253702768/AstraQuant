from app.domain.services.audit_export_builder import AuditExportBuilder
from app.domain.services.audit_redaction_service import AuditRedactionService
from app.domain.services.audit_trace_builder import AuditTraceBuilder

def test_audit_redaction_secret(): assert AuditRedactionService().redact({"secret_key":"x"})["secret_key"] == "[REDACTED]"
def test_audit_trace_builder(): assert AuditTraceBuilder().key({"trace_id":"t"}) == "t"
def test_audit_export_csv(): assert "event_type" in AuditExportBuilder().csv([{"event_type":"A","resource_type":"r","resource_id":"1"}])
def test_audit_export_json(): assert "event_type" in AuditExportBuilder().json([{"event_type":"A"}])
