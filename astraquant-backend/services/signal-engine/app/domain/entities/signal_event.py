from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class SignalEvent:
    id: str | None
    strategy_id: str
    strategy_version_id: str
    exchange: str
    internal_symbol: str
    signal_type: str
    side: str | None
    position_side: str | None
    action: str
    confidence: float
    reference_price: Decimal
    suggested_price: Decimal | None
    suggested_size: Decimal | None
    suggested_position_pct: Decimal | None
    leverage: Decimal
    reason: str
    indicator_snapshot: dict
    market_snapshot: dict
    freshness_snapshot: dict
    risk_hint_json: dict
    status: str
    dedup_key: str
    bar_id: str | None
    created_at: datetime | None = None
