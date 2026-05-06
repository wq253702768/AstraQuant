from app.domain.entities.lifecycle import LifecycleEvidence
from app.domain.enums.evidence_type import EvidenceType


class EvidenceCollector:
    REQUIRED_FOR_SMALL_LIVE = {
        EvidenceType.BACKTEST_REPORT.value,
        EvidenceType.AI_ANALYSIS_REPORT.value,
        EvidenceType.STRATEGY_SCORE.value,
        EvidenceType.SIMULATION_ADMISSION_RESULT.value,
    }
    REQUIRED_FOR_SCALE_UP = REQUIRED_FOR_SMALL_LIVE | {EvidenceType.LIVE_ADMISSION_RESULT.value}

    def missing_for_small_live(self, evidence: list[LifecycleEvidence]) -> list[str]:
        return sorted(self.REQUIRED_FOR_SMALL_LIVE - {item.evidence_type for item in evidence})

    def missing_for_scale_up(self, evidence: list[LifecycleEvidence]) -> list[str]:
        return sorted(self.REQUIRED_FOR_SCALE_UP - {item.evidence_type for item in evidence})

    def summarize(self, evidence: list[LifecycleEvidence]) -> dict:
        return {
            "count": len(evidence),
            "types": sorted({item.evidence_type for item in evidence}),
            "all_passed": all(item.passed is not False for item in evidence),
        }
