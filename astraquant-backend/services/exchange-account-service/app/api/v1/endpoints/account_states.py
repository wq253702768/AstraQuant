from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/exchange-accounts", tags=["account-state"])
@router.get("/{account_id}/state")
async def state(account_id: str, request: Request): return success_response({"account_id":account_id,"freshness_status":"UNKNOWN"}, request)
