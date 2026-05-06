from fastapi import APIRouter, Request
from astra_common.response import success_response

router = APIRouter(prefix="/ai/prompts", tags=["ai"])

@router.get("")
async def prompts(request: Request):
    return success_response({"items": [{"prompt_code": "drawdown_attribution", "version": "v1.0", "agent_name": "drawdown_attribution_agent", "enabled": True}]}, request)
