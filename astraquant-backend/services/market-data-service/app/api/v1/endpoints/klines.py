from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.config import settings
from app.dependencies import get_db_session
from app.infrastructure.repositories.candle_repository import CandleRepository
from app.schemas.kline import KlineResponse

router = APIRouter(prefix="/market-data/klines", tags=["market-data"])

@router.get("")
async def query(
    request: Request,
    exchange: str = "OKX",
    symbol: str = Query(alias="symbol"),
    timeframe: str = "5m",
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    confirm_only: bool = True,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
):
    bounded_limit = min(limit, settings.max_query_limit)
    rows = await CandleRepository(session).query(exchange, symbol, timeframe, start_time, end_time, confirm_only, bounded_limit)
    items = [
        KlineResponse(
            ts=row.open_time,
            open=str(row.open),
            high=str(row.high),
            low=str(row.low),
            close=str(row.close),
            volume=str(row.volume or "0"),
            quote_volume=str(row.volume_ccy_quote or "0"),
        )
        for row in rows
    ]
    return success_response({"items": items}, request)
