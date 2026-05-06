from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base
class SignalEventModel(Base):
    __tablename__="signal_event"
    id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4()))
    strategy_id:Mapped[str]=mapped_column(UUID(as_uuid=False),index=True)
    strategy_version_id:Mapped[str]=mapped_column(UUID(as_uuid=False),index=True)
    exchange:Mapped[str]=mapped_column(String(32))
    internal_symbol:Mapped[str]=mapped_column(String(64),index=True)
    signal_type:Mapped[str]=mapped_column(String(64))
    side:Mapped[str|None]=mapped_column(String(16),nullable=True)
    position_side:Mapped[str|None]=mapped_column(String(16),nullable=True)
    action:Mapped[str]=mapped_column(String(32))
    confidence:Mapped[float|None]=mapped_column(Numeric(8,4),nullable=True)
    reference_price:Mapped[float|None]=mapped_column(Numeric(32,16),nullable=True)
    suggested_price:Mapped[float|None]=mapped_column(Numeric(32,16),nullable=True)
    suggested_size:Mapped[float|None]=mapped_column(Numeric(32,16),nullable=True)
    suggested_position_pct:Mapped[float|None]=mapped_column(Numeric(18,8),nullable=True)
    leverage:Mapped[float|None]=mapped_column(Numeric(8,2),nullable=True)
    reason:Mapped[str|None]=mapped_column(Text,nullable=True)
    indicator_snapshot:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
    market_snapshot:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
    freshness_snapshot:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
    risk_hint_json:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
    status:Mapped[str]=mapped_column(String(64),index=True)
    dedup_key:Mapped[str|None]=mapped_column(String(256),index=True)
    bar_id:Mapped[str|None]=mapped_column(String(128),nullable=True)
    trace_id:Mapped[str|None]=mapped_column(String(128),nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
class StrategyRuntimeStateModel(Base):
    __tablename__="strategy_runtime_state"
    id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4()))
    strategy_id:Mapped[str]=mapped_column(UUID(as_uuid=False))
    strategy_version_id:Mapped[str]=mapped_column(UUID(as_uuid=False),index=True)
    exchange:Mapped[str]=mapped_column(String(32))
    internal_symbol:Mapped[str]=mapped_column(String(64))
    runtime_status:Mapped[str]=mapped_column(String(64),index=True)
    last_signal_id:Mapped[str|None]=mapped_column(UUID(as_uuid=False),nullable=True)
    last_signal_time:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    last_bar_id:Mapped[str|None]=mapped_column(String(128),nullable=True)
    last_error_message:Mapped[str|None]=mapped_column(Text,nullable=True)
    runtime_config:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
