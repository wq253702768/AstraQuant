from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_paper_account_service import CreatePaperAccountService
from app.application.services.query_account_service import QueryAccountService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.account import CreatePaperAccountRequest
router=APIRouter(prefix="/paper-trading/accounts", tags=["paper-trading"])
@router.post("")
async def create(payload: CreatePaperAccountRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await CreatePaperAccountService(session).execute(payload, operator_id); await session.commit(); return success_response(result, request)
@router.get("/{account_id}")
async def get(account_id: str, request: Request, session: AsyncSession=Depends(get_db_session)): return success_response(await QueryAccountService(session).get(account_id), request)
@router.get("/{account_id}/positions")
async def positions(account_id: str, request: Request): return success_response({"items": []}, request)
@router.get("/{account_id}/ledger")
async def ledger(account_id: str, request: Request): return success_response({"items": []}, request)
