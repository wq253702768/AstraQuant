class LifecycleRiskSummaryService:
    def summarize(self, evidence: list[dict]) -> dict:
        failed = [item for item in evidence if item.get("passed") is False]
        high_risk = [item for item in evidence if item.get("risk_level") in {"HIGH", "CRITICAL"}]
        return {
            "failed_evidence_count": len(failed),
            "high_risk_evidence_count": len(high_risk),
            "risk_level": "CRITICAL" if high_risk else ("HIGH" if failed else "LOW"),
        }
