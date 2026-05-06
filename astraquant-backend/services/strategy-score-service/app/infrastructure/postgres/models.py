from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class StrategyScoreModel(Base):
    __tablename__ = "strategy_score"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    backtest_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    ai_task_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    total_score: Mapped[float] = mapped_column(Numeric(8,2))
    grade: Mapped[str] = mapped_column(String(8))
    profit_score: Mapped[float] = mapped_column(Numeric(8,2))
    drawdown_score: Mapped[float] = mapped_column(Numeric(8,2))
    stability_score: Mapped[float] = mapped_column(Numeric(8,2))
    out_of_sample_score: Mapped[float] = mapped_column(Numeric(8,2))
    cost_score: Mapped[float] = mapped_column(Numeric(8,2))
    risk_score: Mapped[float] = mapped_column(Numeric(8,2))
    ai_score: Mapped[float] = mapped_column(Numeric(8,2))
    decision: Mapped[str] = mapped_column(String(64), index=True)
    reject_reasons: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    warnings: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    suggestions: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    detail_json: Mapped[dict] = mapped_column(JSONB)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
