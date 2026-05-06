from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/exchange-accounts", tags=["positions"])
@router.get("/{account_id}/positions")
async def positions(account_id: str, request: Request): return success_response({"items": []}, request)
