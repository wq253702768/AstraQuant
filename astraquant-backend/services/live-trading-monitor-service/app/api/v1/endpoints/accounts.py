from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_account_service import QueryLiveAccountService
router=APIRouter(prefix="/live-monitor/accounts", tags=["live-monitor"])
@router.get("/{account_id}/summary")
async def summary(account_id: str, request: Request): return success_response(await QueryLiveAccountService().execute(account_id), request)
