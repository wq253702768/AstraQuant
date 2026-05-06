from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class MarketDataSyncTaskModel(Base):
    __tablename__ = "market_data_sync_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    exchange: Mapped[str] = mapped_column(String(32), index=True)
    symbols: Mapped[list] = mapped_column(JSONB)
    data_types: Mapped[list] = mapped_column(JSONB)
    timeframes: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    force_resync: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(64), index=True)
    progress: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    current_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class InstrumentConfigModel(Base):
    __tablename__ = "instrument_config"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    exchange: Mapped[str] = mapped_column(String(32), index=True)
    internal_symbol: Mapped[str] = mapped_column(String(64))
    exchange_symbol: Mapped[str] = mapped_column(String(64))
    base_asset: Mapped[str | None] = mapped_column(String(32), nullable=True)
    quote_asset: Mapped[str | None] = mapped_column(String(32), nullable=True)
    margin_asset: Mapped[str | None] = mapped_column(String(32), nullable=True)
    contract_type: Mapped[str] = mapped_column(String(32))
    tick_size: Mapped[float | None] = mapped_column(Numeric(32, 16), nullable=True)
    lot_size: Mapped[float | None] = mapped_column(Numeric(32, 16), nullable=True)
    min_size: Mapped[float | None] = mapped_column(Numeric(32, 16), nullable=True)
    contract_value: Mapped[float | None] = mapped_column(Numeric(32, 16), nullable=True)
    price_precision: Mapped[int | None] = mapped_column(nullable=True)
    size_precision: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    raw_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class DataQualityReportModel(Base):
    __tablename__ = "data_quality_report"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    exchange: Mapped[str] = mapped_column(String(32))
    internal_symbol: Mapped[str] = mapped_column(String(64))
    data_type: Mapped[str] = mapped_column(String(64))
    timeframe: Mapped[str | None] = mapped_column(String(16), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), index=True)
    expected_count: Mapped[int | None] = mapped_column(nullable=True)
    actual_count: Mapped[int | None] = mapped_column(nullable=True)
    missing_count: Mapped[int | None] = mapped_column(nullable=True)
    duplicate_count: Mapped[int | None] = mapped_column(nullable=True)
    abnormal_count: Mapped[int | None] = mapped_column(nullable=True)
    missing_ranges: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    warning_items: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    detail_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
