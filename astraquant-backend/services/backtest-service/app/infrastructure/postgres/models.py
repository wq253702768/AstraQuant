from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base

class BacktestTaskModel(Base):
    __tablename__ = "backtest_task"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    strategy_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), index=True)
    exchange: Mapped[str] = mapped_column(String(32), index=True)
    symbols: Mapped[list] = mapped_column(JSONB)
    timeframe: Mapped[str] = mapped_column(String(16))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    initial_capital: Mapped[float] = mapped_column(Numeric(32, 8))
    cost_model: Mapped[dict] = mapped_column(JSONB)
    risk_model: Mapped[dict] = mapped_column(JSONB)
    data_snapshot_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    params_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    code_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    progress: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    current_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    processed_bars: Mapped[int] = mapped_column(default=0)
    total_bars: Mapped[int] = mapped_column(default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class BacktestResultModel(Base):
    __tablename__ = "backtest_result"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    task_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("backtest_task.id"), unique=True)
    total_return: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    annual_return: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    final_equity: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    max_drawdown: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    max_drawdown_amount: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    win_rate: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    profit_loss_ratio: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    profit_factor: Mapped[float | None] = mapped_column(Numeric(18, 8), nullable=True)
    trade_count: Mapped[int | None] = mapped_column(nullable=True)
    win_trade_count: Mapped[int | None] = mapped_column(nullable=True)
    loss_trade_count: Mapped[int | None] = mapped_column(nullable=True)
    max_consecutive_losses: Mapped[int | None] = mapped_column(nullable=True)
    avg_profit: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    avg_loss: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    fee_total: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    slippage_total: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    funding_fee_total: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    gross_profit: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    gross_loss: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    net_profit: Mapped[float | None] = mapped_column(Numeric(32, 8), nullable=True)
    score: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    decision: Mapped[str | None] = mapped_column(String(64), nullable=True)
    summary_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
