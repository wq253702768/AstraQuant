from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.test_connectivity_service import TestConnectivityService
router=APIRouter(prefix="/exchange-accounts", tags=["connectivity"])
@router.post("/{account_id}/test-connectivity")
async def test(account_id: str, request: Request): return success_response(await TestConnectivityService().execute(account_id), request)
