from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/paper-trading/positions", tags=["paper-trading"])
@router.get("")
async def list_items(request: Request): return success_response({"items": [], "total": 0}, request)
