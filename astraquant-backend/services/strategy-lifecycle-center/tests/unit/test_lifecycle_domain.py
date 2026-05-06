import pytest

from astra_common.errors import AppError
from app.domain.entities.lifecycle import LifecycleApproval, LifecycleEvidence, StrategyLifecycleState
from app.domain.enums.approval_type import ApprovalType
from app.domain.enums.evidence_type import EvidenceType
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus
from app.domain.services.approval_engine import ApprovalEngine
from app.domain.services.lifecycle_decision_builder import LifecycleDecisionBuilder
from app.domain.services.lifecycle_state_machine import LifecycleStateMachine
from app.domain.services.rollback_policy_service import RollbackPolicyService
from app.domain.services.stage_gate_engine import StageGateEngine


def test_init_lifecycle():
    state = StrategyLifecycleState("st_001", "sv_001", "user_001")
    assert state.current_status == StrategyLifecycleStatus.DRAFT.value
    assert state.live_enabled is False


def test_valid_state_transition():
    LifecycleStateMachine().ensure_can_transition("DRAFT", "BACKTESTING")


def test_invalid_state_transition():
    with pytest.raises(AppError):
        LifecycleStateMachine().ensure_can_transition("DRAFT", "SMALL_LIVE_APPROVED")


def test_backtest_gate_pass():
    state = StrategyLifecycleState("st", "sv")
    state.current_status = StrategyLifecycleStatus.BACKTEST_COMPLETED.value
    evidence = [{"evidence_type": EvidenceType.BACKTEST_REPORT.value, "passed": True}]
    result = StageGateEngine().evaluate("BACKTEST_GATE", state, evidence)
    assert result.passed
    assert result.target_status == StrategyLifecycleStatus.AI_REVIEWING.value


def test_score_gate_reject():
    state = StrategyLifecycleState("st", "sv")
    state.current_status = StrategyLifecycleStatus.SCORE_COMPLETED.value
    evidence = [
        {"evidence_type": EvidenceType.STRATEGY_SCORE.value, "passed": True},
        {"evidence_type": EvidenceType.SCORE_ADMISSION_RESULT.value, "passed": False},
    ]
    assert StageGateEngine().evaluate("SCORE_GATE", state, evidence).passed is False


def test_simulation_gate_pass():
    state = StrategyLifecycleState("st", "sv")
    state.current_status = StrategyLifecycleStatus.SIMULATION_COMPLETED.value
    evidence = [{"evidence_type": EvidenceType.SIMULATION_ADMISSION_RESULT.value, "passed": True}]
    assert StageGateEngine().evaluate("SIMULATION_GATE", state, evidence).passed


def test_small_live_application_allowed():
    state = StrategyLifecycleState("st", "sv")
    state.current_status = StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED.value
    evidence = [{"evidence_type": et.value, "passed": True} for et in (
        EvidenceType.BACKTEST_REPORT,
        EvidenceType.AI_ANALYSIS_REPORT,
        EvidenceType.STRATEGY_SCORE,
        EvidenceType.SIMULATION_ADMISSION_RESULT,
    )]
    assert StageGateEngine().evaluate("SMALL_LIVE_GATE", state, evidence).passed


def test_small_live_application_rejected_missing_evidence():
    state = StrategyLifecycleState("st", "sv")
    state.current_status = StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED.value
    result = StageGateEngine().evaluate("SMALL_LIVE_GATE", state, [])
    assert not result.passed
    assert "缺少证据" in result.reject_reasons[0]


def test_approval_approve():
    approval = LifecycleApproval("st", "sv", ApprovalType.SMALL_LIVE_APPLICATION)
    result = ApprovalEngine().approve(approval, "approver", "同意")
    assert result.approval_status == "APPROVED"
    assert result.approved_by == "approver"


def test_approval_reject():
    approval = LifecycleApproval("st", "sv", ApprovalType.SCALE_UP_APPLICATION)
    result = ApprovalEngine().reject(approval, "approver", "风险偏高")
    assert result.approval_status == "REJECTED"
    assert result.rejected_by == "approver"


def test_rollback_to_paper():
    state = StrategyLifecycleState("st", "sv")
    state.live_enabled = True
    state.scale_up_allowed = True
    RollbackPolicyService().rollback_to_paper(state, "订单异常")
    assert state.current_status == "ROLLBACK_TO_PAPER"
    assert state.live_enabled is False


def test_pause_strategy():
    state = StrategyLifecycleState("st", "sv")
    state.live_enabled = True
    RollbackPolicyService().pause(state, "连续熔断")
    assert state.current_status == "PAUSED"
    assert state.live_enabled is False


def test_retire_strategy():
    state = StrategyLifecycleState("st", "sv")
    RollbackPolicyService().retire(state, "长期不达标")
    assert state.current_status == "RETIRED"
    assert state.retired is True


def test_lifecycle_score_calculate():
    evidence = [
        LifecycleEvidence("st", "sv", EvidenceType.BACKTEST_REPORT, "report", "bt", score=80, passed=True),
        LifecycleEvidence("st", "sv", EvidenceType.STRATEGY_SCORE, "score", "sc", score=90, passed=True),
        LifecycleEvidence("st", "sv", EvidenceType.SIMULATION_ADMISSION_RESULT, "paper", "pa", score=85, passed=True),
    ]
    score, risk = LifecycleDecisionBuilder().score(evidence)
    assert score > 0
    assert risk in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
