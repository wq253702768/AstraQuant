from datetime import datetime
from uuid import uuid4
from sqlalchemy import BigInteger, DateTime, Numeric, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class ReportTaskModel(Base):
    __tablename__ = "report_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    report_type: Mapped[str] = mapped_column(String(64))
    related_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    formats: Mapped[list] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(64), index=True)
    progress: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    current_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ReportFileModel(Base):
    __tablename__ = "report_file"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    report_task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("report_task.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(64), index=True)
    related_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    file_format: Mapped[str] = mapped_column(String(16))
    bucket_name: Mapped[str] = mapped_column(String(128))
    object_key: Mapped[str] = mapped_column(String(512))
    file_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
