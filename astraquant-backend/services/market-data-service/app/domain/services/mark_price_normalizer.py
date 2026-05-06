from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

@dataclass(frozen=True)
class NormalizedMarkPrice:
    exchange: str
    internal_symbol: str
    exchange_symbol: str
    mark_price: Decimal
    index_price: Decimal
    ts: datetime

class MarkPriceNormalizer:
    def normalize(self, payload: dict) -> NormalizedMarkPrice:
        return NormalizedMarkPrice(
            exchange=str(payload["exchange"]).upper(),
            internal_symbol=payload["internal_symbol"],
            exchange_symbol=payload["exchange_symbol"],
            mark_price=Decimal(str(payload["mark_price"])),
            index_price=Decimal(str(payload.get("index_price") or "0")),
            ts=datetime.fromtimestamp(int(payload["timestamp"]) / 1000, tz=UTC),
        )
