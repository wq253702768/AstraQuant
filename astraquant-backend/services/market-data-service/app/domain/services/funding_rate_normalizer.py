from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

@dataclass(frozen=True)
class NormalizedFundingRate:
    exchange: str
    internal_symbol: str
    exchange_symbol: str
    funding_rate: Decimal
    realized_rate: Decimal
    funding_time: datetime
    next_funding_time: datetime | None
    mark_price: Decimal

class FundingRateNormalizer:
    def normalize(self, payload: dict) -> NormalizedFundingRate:
        return NormalizedFundingRate(
            exchange=str(payload["exchange"]).upper(),
            internal_symbol=payload["internal_symbol"],
            exchange_symbol=payload["exchange_symbol"],
            funding_rate=Decimal(str(payload.get("funding_rate", "0"))),
            realized_rate=Decimal(str(payload.get("realized_rate") or payload.get("funding_rate") or "0")),
            funding_time=datetime.fromtimestamp(int(payload["funding_time"]) / 1000, tz=UTC),
            next_funding_time=datetime.fromtimestamp(int(payload["next_funding_time"]) / 1000, tz=UTC) if payload.get("next_funding_time") else None,
            mark_price=Decimal(str(payload.get("mark_price") or "0")),
        )
