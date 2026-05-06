from app.domain.services.alert_dedup_service import AlertDedupService
from app.domain.services.alert_escalation_service import AlertEscalationService
from app.domain.services.alert_fingerprint_builder import AlertFingerprintBuilder
from app.domain.services.alert_notification_router import AlertNotificationRouter
from app.domain.services.alert_suppression_service import AlertSuppressionService

def test_alert_fingerprint_builder(): assert AlertFingerprintBuilder().build({"source":"A","rule_code":"R"}) == AlertFingerprintBuilder().build({"rule_code":"R","source":"A"})
def test_alert_dedup_hit(): d=AlertDedupService(); assert not d.hit("x"); assert d.hit("x")
def test_alert_suppression_hit(): assert AlertSuppressionService().suppressed({"suppressed": True})
def test_alert_escalation(): assert AlertEscalationService().escalate("WARNING", 6) == "CRITICAL"
def test_notification_router(): assert "WEBHOOK" in AlertNotificationRouter().channels("CRITICAL")
