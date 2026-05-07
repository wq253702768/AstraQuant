from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.base import Base

class StrategyModel(Base):
    __tablename__ = "strategy"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(128))
    code: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    strategy_type: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    tags: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    latest_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=False))
    updated_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    versions: Mapped[list["StrategyVersionModel"]] = relationship(back_populates="strategy")

class StrategyTemplateModel(Base):
    __tablename__ = "strategy_template"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    strategy_type: Mapped[str] = mapped_column(String(64), index=True)
    template_type: Mapped[str] = mapped_column(String(32), default="CONFIG")
    default_params: Mapped[dict] = mapped_column(JSONB)
    default_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    param_schema: Mapped[dict] = mapped_column(JSONB)
    risk_schema: Mapped[dict] = mapped_column(JSONB)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class StrategyVersionModel(Base):
    __tablename__ = "strategy_version"
    __table_args__ = (UniqueConstraint("strategy_id", "version", name="uk_strategy_version"),)
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("strategy.id"), index=True)
    version: Mapped[str] = mapped_column(String(32))
    template_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("strategy_template.id"))
    params_json: Mapped[dict] = mapped_column(JSONB)
    risk_params_json: Mapped[dict] = mapped_column(JSONB)
    params_hash: Mapped[str] = mapped_column(String(128))
    code_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_source: Mapped[str] = mapped_column(String(64), default="manual")
    status: Mapped[str] = mapped_column(String(64), default="draft", index=True)
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=False))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    strategy: Mapped[StrategyModel] = relationship(back_populates="versions")
    template: Mapped[StrategyTemplateModel] = relationship()

class StrategyStatusLogModel(Base):
    __tablename__ = "strategy_status_log"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("strategy.id"), index=True)
    strategy_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), ForeignKey("strategy_version.id"), nullable=True)
    from_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    to_status: Mapped[str] = mapped_column(String(64))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    operator_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

class StrategyAuditEventBasicModel(Base):
    __tablename__ = "strategy_audit_event_basic"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    event_type: Mapped[str] = mapped_column(String(128), index=True)
    actor_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    actor_username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    action: Mapped[str] = mapped_column(String(128))
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
