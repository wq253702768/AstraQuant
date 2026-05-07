from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models import MarketCandleModel


class CandleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_many(self, rows: list[dict]) -> tuple[int, int]:
        inserted = 0
        updated = 0
        for row in rows:
            stmt = insert(MarketCandleModel).values(**row)
            stmt = stmt.on_conflict_do_update(
                constraint="uk_market_candle",
                set_={
                    "open": stmt.excluded.open,
                    "high": stmt.excluded.high,
                    "low": stmt.excluded.low,
                    "close": stmt.excluded.close,
                    "volume": stmt.excluded.volume,
                    "volume_ccy": stmt.excluded.volume_ccy,
                    "volume_ccy_quote": stmt.excluded.volume_ccy_quote,
                    "confirm": stmt.excluded.confirm,
                    "source": stmt.excluded.source,
                    "sync_job_id": stmt.excluded.sync_job_id,
                    "raw_json": stmt.excluded.raw_json,
                },
            )
            await self.session.execute(stmt)
            updated += 1
        return inserted, updated

    async def query(self, exchange: str, symbol: str, timeframe: str, start_time: datetime | None, end_time: datetime | None, confirm_only: bool, limit: int) -> list[MarketCandleModel]:
        conditions = [
            MarketCandleModel.exchange == exchange,
            MarketCandleModel.internal_symbol == symbol,
            MarketCandleModel.timeframe == timeframe,
        ]
        if start_time:
            conditions.append(MarketCandleModel.open_time >= start_time)
        if end_time:
            conditions.append(MarketCandleModel.open_time < end_time)
        if confirm_only:
            conditions.append(MarketCandleModel.confirm.is_(True))
        result = await self.session.execute(
            select(MarketCandleModel).where(*conditions).order_by(MarketCandleModel.open_time.desc()).limit(limit)
        )
        return list(result.scalars())
