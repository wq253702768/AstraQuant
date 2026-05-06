from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.dependencies import get_db_session
from app.infrastructure.repositories.instrument_repository import InstrumentRepository

router = APIRouter(prefix="/market-data/instruments", tags=["market-data"])

@router.get("")
async def list_instruments(request: Request, exchange: str | None = None, symbol: str | None = None, status: str | None = None, session: AsyncSession = Depends(get_db_session)):
    rows = await InstrumentRepository(session).list(exchange, symbol, status)
    items = [{"exchange": row.exchange, "internal_symbol": row.internal_symbol, "exchange_symbol": row.exchange_symbol, "base_asset": row.base_asset, "quote_asset": row.quote_asset, "margin_asset": row.margin_asset, "contract_type": row.contract_type, "tick_size": str(row.tick_size) if row.tick_size is not None else None, "lot_size": str(row.lot_size) if row.lot_size is not None else None, "min_size": str(row.min_size) if row.min_size is not None else None, "contract_value": str(row.contract_value) if row.contract_value is not None else None, "status": row.status} for row in rows]
    return success_response({"items": items}, request)
