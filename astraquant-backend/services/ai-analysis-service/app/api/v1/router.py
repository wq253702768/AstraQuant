from fastapi import APIRouter
from app.api.v1.endpoints import ai_results, ai_tasks, model_calls, prompts

api_router = APIRouter()
api_router.include_router(ai_tasks.router)
api_router.include_router(ai_results.router)
api_router.include_router(model_calls.router)
api_router.include_router(prompts.router)
