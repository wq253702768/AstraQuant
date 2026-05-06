from app.domain.entities.lifecycle import GateEvaluation, StrategyLifecycleState
from app.domain.enums.evidence_type import EvidenceType
from app.domain.enums.gate_result import GateResult
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


class StageGateEngine:
    REQUIRED_EVIDENCE = {
        "BACKTEST_GATE": [EvidenceType.BACKTEST_REPORT],
        "AI_REVIEW_GATE": [EvidenceType.AI_ANALYSIS_REPORT],
        "SCORE_GATE": [EvidenceType.STRATEGY_SCORE, EvidenceType.SCORE_ADMISSION_RESULT],
        "SIMULATION_GATE": [EvidenceType.SIMULATION_ADMISSION_RESULT],
        "SMALL_LIVE_GATE": [
            EvidenceType.BACKTEST_REPORT,
            EvidenceType.AI_ANALYSIS_REPORT,
            EvidenceType.STRATEGY_SCORE,
            EvidenceType.SIMULATION_ADMISSION_RESULT,
        ],
        "SMALL_LIVE_APPROVAL_GATE": [EvidenceType.APPROVAL_RECORD],
        "LIVE_OBSERVATION_GATE": [EvidenceType.LIVE_TRADING_SUMMARY, EvidenceType.LIVE_ADMISSION_RESULT],
        "SCALE_UP_GATE": [EvidenceType.LIVE_ADMISSION_RESULT],
    }
    TRANSITIONS = {
        "BACKTEST_GATE": (StrategyLifecycleStatus.BACKTEST_COMPLETED, StrategyLifecycleStatus.AI_REVIEWING),
        "AI_REVIEW_GATE": (StrategyLifecycleStatus.AI_REVIEW_COMPLETED, StrategyLifecycleStatus.SCORING),
        "SCORE_GATE": (StrategyLifecycleStatus.SCORE_COMPLETED, StrategyLifecycleStatus.SIMULATION_READY),
        "SIMULATION_GATE": (StrategyLifecycleStatus.SIMULATION_COMPLETED, StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED),
        "SMALL_LIVE_GATE": (StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED, StrategyLifecycleStatus.SMALL_LIVE_APPLICATION_PENDING),
        "SMALL_LIVE_APPROVAL_GATE": (StrategyLifecycleStatus.SMALL_LIVE_APPLICATION_PENDING, StrategyLifecycleStatus.SMALL_LIVE_APPROVED),
        "LIVE_OBSERVATION_GATE": (StrategyLifecycleStatus.SMALL_LIVE_COMPLETED, StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED),
        "SCALE_UP_GATE": (StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED, StrategyLifecycleStatus.SCALE_UP_APPLICATION_PENDING),
    }

    def evaluate(self, gate_code: str, state: StrategyLifecycleState, evidence: list[dict]) -> GateEvaluation:
        if gate_code not in self.TRANSITIONS:
            return GateEvaluation(gate_code, gate_code, GateResult.MANUAL_REVIEW_REQUIRED, False, state.current_status, None, ["未知门禁"])
        expected_from, target = self.TRANSITIONS[gate_code]
        if state.current_status != expected_from.value:
            return GateEvaluation(gate_code, gate_code, GateResult.WAITING, False, expected_from.value, target.value, [f"当前状态 {state.current_status} 尚未到达 {expected_from.value}"])
        existing = {item.get("evidence_type") for item in evidence}
        missing = [item.value for item in self.REQUIRED_EVIDENCE[gate_code] if item.value not in existing]
        failed = [item.get("evidence_type") for item in evidence if item.get("passed") is False and item.get("evidence_type") in {e.value for e in self.REQUIRED_EVIDENCE[gate_code]}]
        if missing:
            return GateEvaluation(gate_code, gate_code, GateResult.WAITING, False, expected_from.value, target.value, [f"缺少证据: {', '.join(missing)}"])
        if failed:
            return GateEvaluation(gate_code, gate_code, GateResult.REJECT, False, expected_from.value, target.value, [f"证据未通过: {', '.join(failed)}"])
        warnings = []
        if gate_code == "SCALE_UP_GATE" and state.risk_level in {"HIGH", "CRITICAL"}:
            return GateEvaluation(gate_code, gate_code, GateResult.MANUAL_REVIEW_REQUIRED, False, expected_from.value, target.value, ["扩大仓位申请风险等级过高"])
        if state.risk_level == "MEDIUM":
            warnings.append("风险等级为 MEDIUM，需要审批时重点关注")
        return GateEvaluation(gate_code, gate_code, GateResult.PASS, True, expected_from.value, target.value, [], warnings)
