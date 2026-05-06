from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.postgres.base import Base


class StrategyLifecycleStateModel(Base):
    __tablename__ = "strategy_lifecycle_state"
    __table_args__ = (UniqueConstraint("strategy_version_id", name="uk_strategy_lifecycle_state"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    current_stage: Mapped[str] = mapped_column(String(64), index=True)
    current_status: Mapped[str] = mapped_column(String(64), index=True)
    backtest_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    ai_analysis_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    strategy_score_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    simulation_observation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    simulation_admission_result_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    live_observation_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    live_admission_result_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    latest_approval_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    latest_gate_result: Mapped[str | None] = mapped_column(String(64), nullable=True)
    latest_gate_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    live_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    scale_up_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    retired: Mapped[bool] = mapped_column(Boolean, default=False)
    risk_level: Mapped[str | None] = mapped_column(String(32), nullable=True)
    lifecycle_score: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class LifecycleEventModel(Base):
    __tablename__ = "lifecycle_event"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    event_type: Mapped[str] = mapped_column(String(128), index=True)
    from_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    to_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    trigger_source: Mapped[str] = mapped_column(String(64))
    trigger_resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    trigger_resource_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    actor_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class LifecycleApprovalModel(Base):
    __tablename__ = "lifecycle_approval"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    approval_type: Mapped[str] = mapped_column(String(64), index=True)
    approval_status: Mapped[str] = mapped_column(String(64), index=True)
    requested_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    approved_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    request_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    approval_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    risk_summary_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LifecycleEvidenceModel(Base):
    __tablename__ = "lifecycle_evidence"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    evidence_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_type: Mapped[str] = mapped_column(String(64))
    resource_id: Mapped[str] = mapped_column(String(128))
    title: Mapped[str | None] = mapped_column(String(256), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    evidence_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    object_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LifecycleTaskModel(Base):
    __tablename__ = "lifecycle_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    task_type: Mapped[str] = mapped_column(String(64))
    task_status: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    related_resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    related_resource_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class LifecycleStageGateResultModel(Base):
    __tablename__ = "lifecycle_stage_gate_result"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    gate_code: Mapped[str] = mapped_column(String(128), index=True)
    gate_name: Mapped[str] = mapped_column(String(128))
    result: Mapped[str] = mapped_column(String(64), index=True)
    from_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    target_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    reject_reasons: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    suggestions: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    evidence_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    trace_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
