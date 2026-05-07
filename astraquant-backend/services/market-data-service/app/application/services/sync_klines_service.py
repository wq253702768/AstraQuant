from datetime import datetime, timezone
from decimal import Decimal

from app.domain.services.timeframe import timeframe_delta
from app.infrastructure.clients.exchange_gateway_client import ExchangeGatewayClient
from app.infrastructure.repositories.candle_repository import CandleRepository
from app.infrastructure.postgres.models import MarketDataSyncTaskModel


def _ms(dt: datetime | None) -> int | None:
    if dt is None:
        return None
    return int(dt.timestamp() * 1000)


def _dt_from_ms(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000, timezone.utc)


class SyncKlinesService:
    def __init__(self, session):
        self.session = session
        self.repo = CandleRepository(session)
        self.client = ExchangeGatewayClient()

    async def sync_task(self, task: MarketDataSyncTaskModel) -> tuple[int, int]:
        inserted = 0
        updated = 0
        for symbol in task.symbols:
            for timeframe in task.timeframes or ["5m"]:
                items = await self.client.get_klines(
                    task.exchange,
                    symbol,
                    timeframe,
                    start_time=_ms(task.start_time),
                    end_time=_ms(task.end_time),
                    limit=300,
                )
                rows = []
                delta = timeframe_delta(timeframe)
                for item in items:
                    ts = int(item.get("timestamp") or item.get("open_time") or 0)
                    if ts <= 0:
                        continue
                    open_time = _dt_from_ms(ts)
                    rows.append(
                        {
                            "exchange": task.exchange,
                            "internal_symbol": symbol,
                            "timeframe": timeframe,
                            "open_time": open_time,
                            "close_time": open_time + delta,
                            "open": Decimal(str(item.get("open", "0"))),
                            "high": Decimal(str(item.get("high", "0"))),
                            "low": Decimal(str(item.get("low", "0"))),
                            "close": Decimal(str(item.get("close", "0"))),
                            "volume": Decimal(str(item.get("volume", "0"))),
                            "volume_ccy": Decimal(str(item.get("volume_ccy", "0"))),
                            "volume_ccy_quote": Decimal(str(item.get("quote_volume", item.get("volume_ccy_quote", "0")))),
                            "confirm": bool(item.get("confirm", True)),
                            "source": "EXCHANGE_ACCESS_GATEWAY",
                            "sync_job_id": task.id,
                            "raw_json": item,
                        }
                    )
                i, u = await self.repo.upsert_many(rows)
                inserted += i
                updated += u
        return inserted, updated
