from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/exchange-accounts", tags=["orders"])
@router.get("/{account_id}/orders")
async def orders(account_id: str, request: Request): return success_response({"items": [], "total": 0}, request)
