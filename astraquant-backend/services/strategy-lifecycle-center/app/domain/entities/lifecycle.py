from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.enums.approval_status import ApprovalStatus
from app.domain.enums.approval_type import ApprovalType
from app.domain.enums.evidence_type import EvidenceType
from app.domain.enums.gate_result import GateResult
from app.domain.enums.lifecycle_stage import LifecycleStage
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class StrategyLifecycleState:
    strategy_id: str
    strategy_version_id: str
    created_by: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    current_stage: str = LifecycleStage.DRAFT.value
    current_status: str = StrategyLifecycleStatus.DRAFT.value
    backtest_id: str | None = None
    ai_analysis_id: str | None = None
    strategy_score_id: str | None = None
    simulation_observation_id: str | None = None
    simulation_admission_result_id: str | None = None
    live_observation_id: str | None = None
    live_admission_result_id: str | None = None
    latest_approval_id: str | None = None
    latest_gate_result: str | None = None
    latest_gate_reason: str | None = None
    live_enabled: bool = False
    scale_up_allowed: bool = False
    retired: bool = False
    risk_level: str | None = None
    lifecycle_score: float | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)


@dataclass
class LifecycleEvent:
    strategy_id: str
    strategy_version_id: str
    event_type: str
    trigger_source: str
    from_status: str | None = None
    to_status: str | None = None
    reason: str | None = None
    trigger_resource_type: str | None = None
    trigger_resource_id: str | None = None
    evidence_json: dict | None = None
    metadata_json: dict | None = None
    actor_id: str | None = None
    trace_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=utcnow)


@dataclass
class LifecycleEvidence:
    strategy_id: str
    strategy_version_id: str
    evidence_type: str | EvidenceType
    resource_type: str
    resource_id: str
    title: str | None = None
    summary: str | None = None
    score: float | None = None
    passed: bool | None = None
    evidence_json: dict | None = None
    object_key: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if isinstance(self.evidence_type, EvidenceType):
            self.evidence_type = self.evidence_type.value


@dataclass
class LifecycleApproval:
    strategy_id: str
    strategy_version_id: str
    approval_type: str | ApprovalType
    requested_by: str | None = None
    request_reason: str | None = None
    evidence_json: dict | None = None
    risk_summary_json: dict | None = None
    expires_at: datetime | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    approval_status: str = ApprovalStatus.PENDING.value
    requested_at: datetime = field(default_factory=utcnow)
    approved_by: str | None = None
    approved_at: datetime | None = None
    rejected_by: str | None = None
    rejected_at: datetime | None = None
    approval_comment: str | None = None
    rejection_reason: str | None = None
    created_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if isinstance(self.approval_type, ApprovalType):
            self.approval_type = self.approval_type.value


@dataclass
class LifecycleTask:
    strategy_id: str
    strategy_version_id: str
    task_type: str
    title: str
    description: str | None = None
    owner_id: str | None = None
    due_at: datetime | None = None
    related_resource_type: str | None = None
    related_resource_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    task_status: str = "PENDING"
    completed_at: datetime | None = None
    completed_by: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)


@dataclass
class LifecycleStageGateResult:
    strategy_id: str
    strategy_version_id: str
    gate_code: str
    gate_name: str
    result: str | GateResult
    from_status: str | None = None
    target_status: str | None = None
    passed: bool = False
    reject_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    evidence_json: dict | None = None
    trace_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    evaluated_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if isinstance(self.result, GateResult):
            self.result = self.result.value


@dataclass
class GateEvaluation:
    gate_code: str
    gate_name: str
    result: str | GateResult
    passed: bool
    from_status: str | None
    target_status: str | None
    reject_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if isinstance(self.result, GateResult):
            self.result = self.result.value
