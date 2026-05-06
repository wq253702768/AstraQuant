from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Numeric, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class AITaskModel(Base):
    __tablename__ = "ai_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    task_type: Mapped[str] = mapped_column(String(64))
    related_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    strategy_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    strategy_version_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    current_agent: Mapped[str | None] = mapped_column(String(128), nullable=True)
    progress: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    input_data_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    result_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AIAgentOutputModel(Base):
    __tablename__ = "ai_agent_output"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    ai_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("ai_task.id"), index=True)
    agent_name: Mapped[str] = mapped_column(String(128), index=True)
    conclusion: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    suggestions_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(8,4), nullable=True)
    output_json: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AIModelCallLogModel(Base):
    __tablename__ = "ai_model_call_log"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    ai_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("ai_task.id"), index=True)
    agent_name: Mapped[str] = mapped_column(String(128), index=True)
    model_provider: Mapped[str] = mapped_column(String(64))
    model_name: Mapped[str] = mapped_column(String(128))
    model_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    temperature: Mapped[float | None] = mapped_column(Numeric(8,4), nullable=True)
    max_context: Mapped[int | None] = mapped_column(nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    input_data_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    request_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

class AIPromptVersionModel(Base):
    __tablename__ = "ai_prompt_version"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    prompt_code: Mapped[str] = mapped_column(String(128))
    version: Mapped[str] = mapped_column(String(32))
    agent_name: Mapped[str] = mapped_column(String(128), index=True)
    content: Mapped[str] = mapped_column(Text)
    output_schema: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
