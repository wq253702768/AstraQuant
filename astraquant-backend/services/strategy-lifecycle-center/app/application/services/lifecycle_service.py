from dataclasses import asdict
from datetime import timedelta

from astra_common.errors import AppError
from app.config import settings
from app.domain.entities.lifecycle import (
    LifecycleApproval,
    LifecycleEvent,
    LifecycleEvidence,
    LifecycleStageGateResult,
    LifecycleTask,
    StrategyLifecycleState,
    utcnow,
)
from app.domain.enums.approval_status import ApprovalStatus
from app.domain.enums.approval_type import ApprovalType
from app.domain.enums.evidence_type import EvidenceType
from app.domain.enums.gate_result import GateResult
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus
from app.domain.services.approval_engine import ApprovalEngine
from app.domain.services.lifecycle_decision_builder import LifecycleDecisionBuilder
from app.domain.services.lifecycle_state_machine import LifecycleStateMachine
from app.domain.services.lifecycle_timeline_builder import LifecycleTimelineBuilder
from app.domain.services.stage_gate_engine import StageGateEngine


class LifecycleStore:
    def __init__(self) -> None:
        self.states: dict[str, StrategyLifecycleState] = {}
        self.events: list[LifecycleEvent] = []
        self.evidence: dict[str, list[LifecycleEvidence]] = {}
        self.approvals: dict[str, LifecycleApproval] = {}
        self.tasks: dict[str, list[LifecycleTask]] = {}
        self.gates: list[LifecycleStageGateResult] = []

    def clear(self) -> None:
        self.__init__()


store = LifecycleStore()


class LifecycleService:
    def __init__(self, data: LifecycleStore = store) -> None:
        self.store = data
        self.state_machine = LifecycleStateMachine()
        self.gate_engine = StageGateEngine()
        self.approvals = ApprovalEngine()
        self.decisions = LifecycleDecisionBuilder()

    def init_lifecycle(self, strategy_id: str, strategy_version_id: str, created_by: str | None = None, trace_id: str | None = None) -> StrategyLifecycleState:
        if strategy_version_id in self.store.states:
            return self.store.states[strategy_version_id]
        state = StrategyLifecycleState(strategy_id=strategy_id, strategy_version_id=strategy_version_id, created_by=created_by)
        self.store.states[strategy_version_id] = state
        self._event(state, "LIFECYCLE_INITIALIZED", None, state.current_status, "SYSTEM_EVENT", "策略版本创建", created_by, trace_id)
        return state

    def get_state(self, strategy_version_id: str) -> StrategyLifecycleState:
        state = self.store.states.get(strategy_version_id)
        if not state:
            raise AppError("LIFECYCLE_NOT_FOUND", "生命周期记录不存在", 404)
        return state

    def transition(
        self,
        strategy_version_id: str,
        to_status: str | StrategyLifecycleStatus,
        reason: str,
        trigger_source: str = "SYSTEM_EVENT",
        actor_id: str | None = None,
        trace_id: str | None = None,
    ) -> StrategyLifecycleState:
        state = self.get_state(strategy_version_id)
        from_status = state.current_status
        self.state_machine.ensure_can_transition(from_status, to_status)
        target = StrategyLifecycleStatus(to_status)
        state.current_status = target.value
        state.current_stage = self.state_machine.stage_for_status(target).value
        if target in {StrategyLifecycleStatus.ROLLBACK_TO_PAPER, StrategyLifecycleStatus.PAUSED, StrategyLifecycleStatus.RETIRED}:
            state.live_enabled = False
            state.scale_up_allowed = False
        if target == StrategyLifecycleStatus.RETIRED:
            state.retired = True
        if target == StrategyLifecycleStatus.SMALL_LIVE_APPROVED:
            state.live_enabled = True
        if target == StrategyLifecycleStatus.SCALE_UP_APPROVED:
            state.scale_up_allowed = True
        state.updated_at = utcnow()
        self._event(state, "LIFECYCLE_STATE_CHANGED", from_status, state.current_status, trigger_source, reason, actor_id, trace_id)
        return state

    def add_evidence(self, strategy_version_id: str, evidence: LifecycleEvidence | dict) -> LifecycleEvidence:
        state = self.get_state(strategy_version_id)
        if isinstance(evidence, dict):
            evidence = LifecycleEvidence(
                strategy_id=state.strategy_id,
                strategy_version_id=strategy_version_id,
                evidence_type=evidence["evidence_type"],
                resource_type=evidence.get("resource_type", evidence["evidence_type"].lower()),
                resource_id=evidence.get("resource_id", evidence.get("id", evidence["evidence_type"].lower())),
                title=evidence.get("title"),
                summary=evidence.get("summary"),
                score=evidence.get("score"),
                passed=evidence.get("passed"),
                evidence_json=evidence.get("evidence_json"),
                object_key=evidence.get("object_key"),
            )
        if evidence.strategy_id != state.strategy_id or evidence.strategy_version_id != state.strategy_version_id:
            raise AppError("EVIDENCE_NOT_FOUND", "证据与生命周期策略版本不匹配", 400)
        self.store.evidence.setdefault(strategy_version_id, []).append(evidence)
        return evidence

    def evaluate_gate(self, strategy_version_id: str, gate_code: str, trace_id: str | None = None) -> LifecycleStageGateResult:
        state = self.get_state(strategy_version_id)
        evidence = [asdict(item) for item in self.store.evidence.get(strategy_version_id, [])]
        result = self.gate_engine.evaluate(gate_code, state, evidence)
        gate = LifecycleStageGateResult(
            strategy_id=state.strategy_id,
            strategy_version_id=state.strategy_version_id,
            gate_code=gate_code,
            gate_name=gate_code,
            result=result.result,
            from_status=result.from_status,
            target_status=result.target_status,
            passed=result.passed,
            reject_reasons=result.reject_reasons,
            warnings=result.warnings,
            suggestions=result.suggestions,
            evidence_json={"evidence_types": [item.get("evidence_type") for item in evidence]},
            trace_id=trace_id,
        )
        self.store.gates.append(gate)
        state.latest_gate_result = gate.result
        state.latest_gate_reason = "; ".join(gate.reject_reasons + gate.warnings) or None
        if gate.passed and gate.target_status:
            self.transition(strategy_version_id, gate.target_status, f"{gate_code} 通过", "STAGE_GATE", trace_id=trace_id)
        elif gate.result in {GateResult.REJECT.value, GateResult.MANUAL_REVIEW_REQUIRED.value}:
            self._event(state, "LIFECYCLE_GATE_FAILED", state.current_status, state.current_status, "STAGE_GATE", state.latest_gate_reason or "门禁未通过", trace_id=trace_id)
        return gate

    def create_application(self, strategy_version_id: str, approval_type: str | ApprovalType, request_reason: str | None, requested_by: str | None, trace_id: str | None = None) -> dict:
        state = self.get_state(strategy_version_id)
        approval_type_value = ApprovalType(approval_type)
        evidence = [asdict(item) for item in self.store.evidence.get(strategy_version_id, [])]
        decision = self.approvals.check_application_allowed(approval_type_value, state, evidence)
        if not decision.allowed:
            code = "SMALL_LIVE_APPLICATION_NOT_ALLOWED" if approval_type_value == ApprovalType.SMALL_LIVE_APPLICATION else "SCALE_UP_APPLICATION_NOT_ALLOWED"
            raise AppError(code, "; ".join(decision.reasons), 409, {"missing_evidence": decision.missing_evidence})
        for approval in self.store.approvals.values():
            if approval.strategy_version_id == strategy_version_id and approval.approval_type == approval_type_value.value and approval.approval_status == ApprovalStatus.PENDING.value:
                raise AppError("APPROVAL_ALREADY_PROCESSED", "该申请已有待处理审批", 409)
        expire_days = settings.default_scale_up_approval_expire_days if approval_type_value == ApprovalType.SCALE_UP_APPLICATION else settings.default_small_live_approval_expire_days
        approval = LifecycleApproval(
            strategy_id=state.strategy_id,
            strategy_version_id=strategy_version_id,
            approval_type=approval_type_value,
            requested_by=requested_by,
            request_reason=request_reason,
            evidence_json={"items": evidence},
            risk_summary_json={"risk_level": state.risk_level, "lifecycle_score": state.lifecycle_score},
            expires_at=utcnow() + timedelta(days=expire_days),
        )
        self.store.approvals[approval.id] = approval
        state.latest_approval_id = approval.id
        target = StrategyLifecycleStatus.SMALL_LIVE_APPLICATION_PENDING if approval_type_value == ApprovalType.SMALL_LIVE_APPLICATION else StrategyLifecycleStatus.SCALE_UP_APPLICATION_PENDING
        self.transition(strategy_version_id, target, request_reason or "发起生命周期申请", "USER_ACTION", requested_by, trace_id)
        self._event(state, "LIFECYCLE_APPROVAL_CREATED", None, state.current_status, "USER_ACTION", request_reason, requested_by, trace_id, {"approval_id": approval.id})
        return {"approval_id": approval.id, "approval_type": approval.approval_type, "approval_status": approval.approval_status}

    def approve(self, approval_id: str, approved_by: str | None, comment: str | None, trace_id: str | None = None) -> dict:
        approval = self._approval(approval_id)
        if approval.approval_status != ApprovalStatus.PENDING.value:
            raise AppError("APPROVAL_ALREADY_PROCESSED", "审批已处理", 409)
        approval.approval_status = ApprovalStatus.APPROVED.value
        approval.approved_by = approved_by
        approval.approved_at = utcnow()
        approval.approval_comment = comment
        target = StrategyLifecycleStatus.SMALL_LIVE_APPROVED if approval.approval_type == ApprovalType.SMALL_LIVE_APPLICATION.value else StrategyLifecycleStatus.SCALE_UP_APPROVED
        self.add_evidence(approval.strategy_version_id, LifecycleEvidence(approval.strategy_id, approval.strategy_version_id, EvidenceType.APPROVAL_RECORD, "lifecycle_approval", approval.id, "审批记录", passed=True))
        state = self.transition(approval.strategy_version_id, target, comment or "审批通过", "USER_ACTION", approved_by, trace_id)
        self._event(state, "LIFECYCLE_APPROVAL_APPROVED", None, state.current_status, "USER_ACTION", comment, approved_by, trace_id, {"approval_id": approval.id})
        return {"approval_id": approval.id, "approval_status": approval.approval_status, "new_status": state.current_status}

    def reject(self, approval_id: str, rejected_by: str | None, reason: str | None, trace_id: str | None = None) -> dict:
        approval = self._approval(approval_id)
        if approval.approval_status != ApprovalStatus.PENDING.value:
            raise AppError("APPROVAL_ALREADY_PROCESSED", "审批已处理", 409)
        approval.approval_status = ApprovalStatus.REJECTED.value
        approval.rejected_by = rejected_by
        approval.rejected_at = utcnow()
        approval.rejection_reason = reason
        target = StrategyLifecycleStatus.SMALL_LIVE_REJECTED if approval.approval_type == ApprovalType.SMALL_LIVE_APPLICATION.value else StrategyLifecycleStatus.SCALE_UP_REJECTED
        state = self.transition(approval.strategy_version_id, target, reason or "审批拒绝", "USER_ACTION", rejected_by, trace_id)
        self._event(state, "LIFECYCLE_APPROVAL_REJECTED", None, state.current_status, "USER_ACTION", reason, rejected_by, trace_id, {"approval_id": approval.id})
        return {"approval_id": approval.id, "approval_status": approval.approval_status, "new_status": state.current_status}

    def rollback_to_paper(self, strategy_version_id: str, reason: str | None, actor_id: str | None = None, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.transition(strategy_version_id, StrategyLifecycleStatus.ROLLBACK_TO_PAPER, reason or "回退模拟盘", "USER_ACTION", actor_id, trace_id)
        self.store.tasks.setdefault(strategy_version_id, []).append(LifecycleTask(state.strategy_id, strategy_version_id, "SIMULATION_OBSERVATION", "重新模拟盘观察", reason))
        return state

    def pause(self, strategy_version_id: str, reason: str | None, actor_id: str | None = None, trace_id: str | None = None) -> StrategyLifecycleState:
        return self.transition(strategy_version_id, StrategyLifecycleStatus.PAUSED, reason or "暂停策略", "USER_ACTION", actor_id, trace_id)

    def retire(self, strategy_version_id: str, reason: str | None, actor_id: str | None = None, trace_id: str | None = None) -> StrategyLifecycleState:
        return self.transition(strategy_version_id, StrategyLifecycleStatus.RETIRED, reason or "归档策略", "USER_ACTION", actor_id, trace_id)

    def apply_live_admission(self, strategy_version_id: str, result: dict, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.get_state(strategy_version_id)
        state.live_observation_id = result.get("live_observation_id")
        state.live_admission_result_id = result.get("live_admission_result_id") or result.get("id")
        decision = self.decisions.status_for_live_admission(result)
        return self.transition(strategy_version_id, decision, result.get("reason", "实盘观察评估完成"), "SYSTEM_EVENT", trace_id=trace_id)

    def consume_backtest_completed(self, payload: dict, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.init_lifecycle(payload["strategy_id"], payload["strategy_version_id"], trace_id=trace_id)
        state.backtest_id = payload.get("backtest_id")
        self.add_evidence(state.strategy_version_id, LifecycleEvidence(state.strategy_id, state.strategy_version_id, EvidenceType.BACKTEST_REPORT, "backtest_report", state.backtest_id or "backtest", "回测报告", score=payload.get("score"), passed=payload.get("passed", True)))
        return self.transition(state.strategy_version_id, StrategyLifecycleStatus.BACKTEST_COMPLETED, "回测完成", "SYSTEM_EVENT", trace_id=trace_id)

    def consume_ai_analysis_completed(self, payload: dict, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.get_state(payload["strategy_version_id"])
        if state.current_status == StrategyLifecycleStatus.BACKTEST_COMPLETED.value:
            self.transition(state.strategy_version_id, StrategyLifecycleStatus.AI_REVIEWING, "进入 AI 复盘", "STAGE_GATE", trace_id=trace_id)
        state.ai_analysis_id = payload.get("ai_analysis_id")
        self.add_evidence(state.strategy_version_id, LifecycleEvidence(state.strategy_id, state.strategy_version_id, EvidenceType.AI_ANALYSIS_REPORT, "ai_analysis_report", state.ai_analysis_id or "ai_analysis", "AI 复盘报告", score=payload.get("score"), passed=payload.get("passed", True)))
        return self.transition(state.strategy_version_id, StrategyLifecycleStatus.AI_REVIEW_COMPLETED, "AI 复盘完成", "SYSTEM_EVENT", trace_id=trace_id)

    def consume_strategy_score_calculated(self, payload: dict, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.get_state(payload["strategy_version_id"])
        if state.current_status == StrategyLifecycleStatus.AI_REVIEW_COMPLETED.value:
            self.transition(state.strategy_version_id, StrategyLifecycleStatus.SCORING, "进入策略评分", "STAGE_GATE", trace_id=trace_id)
        state.strategy_score_id = payload.get("strategy_score_id")
        self.transition(state.strategy_version_id, StrategyLifecycleStatus.SCORE_COMPLETED, "策略评分完成", "SYSTEM_EVENT", trace_id=trace_id)
        score = payload.get("score", 0)
        passed = payload.get("passed", score >= 80)
        self.add_evidence(state.strategy_version_id, LifecycleEvidence(state.strategy_id, state.strategy_version_id, EvidenceType.STRATEGY_SCORE, "strategy_score", state.strategy_score_id or "score", "策略评分", score=score, passed=passed))
        self.add_evidence(state.strategy_version_id, LifecycleEvidence(state.strategy_id, state.strategy_version_id, EvidenceType.SCORE_ADMISSION_RESULT, "score_admission_result", state.strategy_score_id or "score_admission", "评分准入结果", score=score, passed=passed))
        if passed:
            self.evaluate_gate(state.strategy_version_id, "SCORE_GATE", trace_id)
        else:
            self.transition(state.strategy_version_id, StrategyLifecycleStatus.SCORE_REJECTED, "评分不足", "STAGE_GATE", trace_id=trace_id)
        return self.get_state(state.strategy_version_id)

    def consume_simulation_admission(self, payload: dict, trace_id: str | None = None) -> StrategyLifecycleState:
        state = self.get_state(payload["strategy_version_id"])
        state.simulation_admission_result_id = payload.get("simulation_admission_result_id")
        passed = payload.get("passed", True)
        self.add_evidence(state.strategy_version_id, LifecycleEvidence(state.strategy_id, state.strategy_version_id, EvidenceType.SIMULATION_ADMISSION_RESULT, "simulation_admission_result", state.simulation_admission_result_id or "simulation_admission", "模拟盘准入结果", score=payload.get("score"), passed=passed))
        if passed:
            self.evaluate_gate(state.strategy_version_id, "SIMULATION_GATE", trace_id)
        else:
            self.transition(state.strategy_version_id, StrategyLifecycleStatus.SIMULATION_REJECTED, "模拟盘准入未通过", "STAGE_GATE", trace_id=trace_id)
        return self.get_state(state.strategy_version_id)

    def list_states(self, filters: dict) -> dict:
        items = list(self.store.states.values())
        for key in ["current_status", "current_stage", "strategy_id", "strategy_version_id"]:
            if filters.get(key):
                items = [item for item in items if getattr(item, key) == filters[key]]
        if filters.get("live_enabled") is not None:
            items = [item for item in items if item.live_enabled == self._bool(filters["live_enabled"])]
        if filters.get("retired") is not None:
            items = [item for item in items if item.retired == self._bool(filters["retired"])]
        page = int(filters.get("page", 1))
        page_size = int(filters.get("page_size", 20))
        start = (page - 1) * page_size
        return {"items": items[start : start + page_size], "total": len(items)}

    def timeline(self, strategy_version_id: str) -> dict:
        self.get_state(strategy_version_id)
        return {"items": LifecycleTimelineBuilder().build(self.store.events, strategy_version_id)}

    def evidence(self, strategy_version_id: str) -> dict:
        self.get_state(strategy_version_id)
        return {"items": [asdict(item) for item in self.store.evidence.get(strategy_version_id, [])]}

    def dashboard(self) -> dict:
        states = list(self.store.states.values())
        pending = [item for item in self.store.approvals.values() if item.approval_status == ApprovalStatus.PENDING.value]
        return {
            "total_strategy_versions": len(states),
            "draft_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.DRAFT.value),
            "backtesting_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.BACKTESTING.value),
            "simulation_running_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.SIMULATION_RUNNING.value),
            "simulation_passed_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED.value),
            "small_live_running_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.SMALL_LIVE_RUNNING.value),
            "paused_count": sum(1 for item in states if item.current_status == StrategyLifecycleStatus.PAUSED.value),
            "retired_count": sum(1 for item in states if item.retired),
            "pending_approval_count": len(pending),
            "high_risk_count": sum(1 for item in states if item.risk_level in {"HIGH", "CRITICAL"}),
        }

    def _approval(self, approval_id: str) -> LifecycleApproval:
        approval = self.store.approvals.get(approval_id)
        if not approval:
            raise AppError("APPROVAL_NOT_FOUND", "审批不存在", 404)
        return approval

    def _event(
        self,
        state: StrategyLifecycleState,
        event_type: str,
        from_status: str | None,
        to_status: str | None,
        trigger_source: str,
        reason: str | None,
        actor_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        self.store.events.append(
            LifecycleEvent(
                strategy_id=state.strategy_id,
                strategy_version_id=state.strategy_version_id,
                event_type=event_type,
                from_status=from_status,
                to_status=to_status,
                trigger_source=trigger_source,
                reason=reason,
                actor_id=actor_id,
                trace_id=trace_id,
                metadata_json=metadata,
            )
        )

    @staticmethod
    def _bool(value: object) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).lower() in {"1", "true", "yes"}


lifecycle_service = LifecycleService()
