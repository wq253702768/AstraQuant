from fastapi import APIRouter, Request
from astra_common.response import success_response

router = APIRouter(prefix="/market-data/klines", tags=["market-data"])

@router.get("")
async def query(request: Request):
    return success_response({"items": []}, request)
