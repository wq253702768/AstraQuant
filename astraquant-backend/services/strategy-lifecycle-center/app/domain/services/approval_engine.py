from dataclasses import dataclass

from astra_common.errors import AppError
from app.domain.entities.lifecycle import LifecycleApproval, StrategyLifecycleState, utcnow
from app.domain.enums.approval_status import ApprovalStatus
from app.domain.enums.approval_type import ApprovalType
from app.domain.enums.evidence_type import EvidenceType
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


@dataclass
class ApplicationDecision:
    allowed: bool
    reasons: list[str]
    missing_evidence: list[str]


class ApprovalEngine:
    SMALL_LIVE_REQUIRED = {
        EvidenceType.BACKTEST_REPORT.value,
        EvidenceType.AI_ANALYSIS_REPORT.value,
        EvidenceType.STRATEGY_SCORE.value,
        EvidenceType.SIMULATION_ADMISSION_RESULT.value,
    }
    SCALE_UP_REQUIRED = {EvidenceType.LIVE_ADMISSION_RESULT.value}

    def check_application_allowed(self, approval_type: ApprovalType, state: StrategyLifecycleState, evidence: list[dict]) -> ApplicationDecision:
        if state.retired:
            return ApplicationDecision(False, ["策略已归档"], [])
        existing = {item.get("evidence_type") for item in evidence if item.get("passed") is not False}
        if approval_type == ApprovalType.SMALL_LIVE_APPLICATION:
            if state.current_status != StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED.value:
                return ApplicationDecision(False, ["当前状态不允许申请小仓实盘"], [])
            missing = sorted(self.SMALL_LIVE_REQUIRED - existing)
            return ApplicationDecision(not missing, ["缺少小仓实盘申请证据"] if missing else [], missing)
        if approval_type == ApprovalType.SCALE_UP_APPLICATION:
            if state.current_status != StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED.value:
                return ApplicationDecision(False, ["当前状态不允许申请扩大仓位"], [])
            missing = sorted(self.SCALE_UP_REQUIRED - existing)
            if state.risk_level in {"HIGH", "CRITICAL"}:
                return ApplicationDecision(False, ["扩大仓位申请风险过高"], missing)
            return ApplicationDecision(not missing, ["缺少扩大仓位申请证据"] if missing else [], missing)
        return ApplicationDecision(False, ["审批类型不支持申请"], [])

    def approve(self, approval: LifecycleApproval, approved_by: str | None, comment: str | None = None) -> LifecycleApproval:
        self._ensure_pending(approval)
        approval.approval_status = ApprovalStatus.APPROVED.value
        approval.approved_by = approved_by
        approval.approved_at = utcnow()
        approval.approval_comment = comment
        return approval

    def reject(self, approval: LifecycleApproval, rejected_by: str | None, reason: str | None = None) -> LifecycleApproval:
        self._ensure_pending(approval)
        approval.approval_status = ApprovalStatus.REJECTED.value
        approval.rejected_by = rejected_by
        approval.rejected_at = utcnow()
        approval.rejection_reason = reason
        return approval

    @staticmethod
    def approved_target(approval_type: str) -> StrategyLifecycleStatus:
        return StrategyLifecycleStatus.SMALL_LIVE_APPROVED if approval_type == ApprovalType.SMALL_LIVE_APPLICATION.value else StrategyLifecycleStatus.SCALE_UP_APPROVED

    @staticmethod
    def rejected_target(approval_type: str) -> StrategyLifecycleStatus:
        return StrategyLifecycleStatus.SMALL_LIVE_REJECTED if approval_type == ApprovalType.SMALL_LIVE_APPLICATION.value else StrategyLifecycleStatus.SCALE_UP_REJECTED

    @staticmethod
    def _ensure_pending(approval: LifecycleApproval) -> None:
        if approval.approval_status != ApprovalStatus.PENDING.value:
            raise AppError("APPROVAL_ALREADY_PROCESSED", "审批已处理", 409)
