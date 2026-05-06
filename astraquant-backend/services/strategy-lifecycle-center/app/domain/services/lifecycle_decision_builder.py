from dataclasses import asdict
from decimal import Decimal

from app.domain.entities.lifecycle import LifecycleEvidence
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


class LifecycleDecisionBuilder:
    WEIGHTS = {
        "BACKTEST_REPORT": Decimal("0.20"),
        "AI_ANALYSIS_REPORT": Decimal("0.10"),
        "STRATEGY_SCORE": Decimal("0.20"),
        "SIMULATION_ADMISSION_RESULT": Decimal("0.20"),
        "LIVE_ADMISSION_RESULT": Decimal("0.20"),
        "RISK_EVENT_SUMMARY": Decimal("0.10"),
    }

    def score(self, evidence: list[LifecycleEvidence | dict]) -> tuple[float, str]:
        weighted = Decimal("0")
        weight_total = Decimal("0")
        for raw in evidence:
            item = asdict(raw) if isinstance(raw, LifecycleEvidence) else raw
            evidence_type = item.get("evidence_type")
            value = item.get("score")
            if evidence_type in self.WEIGHTS and value is not None:
                weighted += Decimal(str(value)) * self.WEIGHTS[evidence_type]
                weight_total += self.WEIGHTS[evidence_type]
        result = Decimal("0") if weight_total == 0 else (weighted / weight_total).quantize(Decimal("0.01"))
        return float(result), self.risk_level(result)

    def status_for_live_admission(self, payload: dict) -> StrategyLifecycleStatus:
        decision = payload.get("decision")
        if decision == "ALLOW_SCALE_UP_APPLICATION":
            return StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED
        if decision == "ROLLBACK_TO_PAPER":
            return StrategyLifecycleStatus.ROLLBACK_TO_PAPER
        if decision == "PAUSE_STRATEGY":
            return StrategyLifecycleStatus.PAUSED
        return StrategyLifecycleStatus.SMALL_LIVE_RUNNING

    @staticmethod
    def risk_level(score: Decimal) -> str:
        if score >= Decimal("85"):
            return "LOW"
        if score >= Decimal("70"):
            return "MEDIUM"
        if score >= Decimal("50"):
            return "HIGH"
        return "CRITICAL"
