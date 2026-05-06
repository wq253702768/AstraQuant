from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/live-monitor/admission-results", tags=["live-monitor"])
@router.get("/{result_id}")
async def query(result_id: str, request: Request): return success_response({"live_admission_result_id": result_id, "decision":"CONTINUE_SMALL_LIVE", "approval_required": True}, request)
