from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class ReplayBuildTaskModel(Base):
    __tablename__ = "replay_build_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    backtest_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    progress: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    current_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
