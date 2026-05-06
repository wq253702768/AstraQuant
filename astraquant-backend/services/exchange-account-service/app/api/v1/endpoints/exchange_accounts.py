from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_exchange_account_service import CreateExchangeAccountService
from app.application.services.disable_exchange_account_service import DisableExchangeAccountService
from app.application.services.enable_exchange_account_service import EnableExchangeAccountService
from app.dependencies import get_db_session, get_operator_id
from app.infrastructure.repositories.exchange_account_repository import ExchangeAccountRepository
from app.schemas.exchange_account import CreateExchangeAccountRequest
router=APIRouter(prefix="/exchange-accounts", tags=["exchange-accounts"])
@router.post("")
async def create(payload: CreateExchangeAccountRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await CreateExchangeAccountService(session).execute(payload,operator_id); await session.commit(); return success_response(result,request)
@router.get("")
async def list_accounts(request: Request, session: AsyncSession=Depends(get_db_session)):
    rows=await ExchangeAccountRepository(session).list(); return success_response({"items":[{"account_id":r.id,"name":r.name,"exchange":r.exchange,"environment":r.environment,"status":r.status,"trading_enabled":r.trading_enabled,"last_connectivity_status":r.last_connectivity_status} for r in rows],"total":len(rows)},request)
@router.post("/{account_id}/enable")
async def enable(account_id: str, payload: dict, request: Request): return success_response(await EnableExchangeAccountService().execute(account_id,payload.get("mode","READ_ONLY")),request)
@router.post("/{account_id}/disable")
async def disable(account_id: str, payload: dict, request: Request): return success_response(await DisableExchangeAccountService().execute(account_id,payload.get("reason","")),request)
