from fastapi import APIRouter, Request
from app.clients.ai_client import AIClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["ai"])

@router.post("/api/ai/backtest-analysis")
async def create(payload: dict, request: Request):
    require_permission(request, "ai:run")
    return await AIClient().request("POST", "/ai/backtest-analysis", request, payload)

@router.get("/api/ai/tasks/{ai_task_id}/status")
async def status(ai_task_id: str, request: Request):
    require_permission(request, "ai:read")
    return await AIClient().request("GET", f"/ai/tasks/{ai_task_id}/status", request)

@router.get("/api/ai/tasks/{ai_task_id}/result")
async def result(ai_task_id: str, request: Request):
    require_permission(request, "ai:read")
    return await AIClient().request("GET", f"/ai/tasks/{ai_task_id}/result", request)

@router.get("/api/ai/tasks/{ai_task_id}/model-calls")
async def model_calls(ai_task_id: str, request: Request):
    require_permission(request, "ai:read")
    return await AIClient().request("GET", f"/ai/tasks/{ai_task_id}/model-calls", request)

@router.get("/api/ai/prompts")
async def prompts(request: Request):
    require_permission(request, "ai:read")
    return await AIClient().request("GET", "/ai/prompts", request)
