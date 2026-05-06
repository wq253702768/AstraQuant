from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.dependencies import get_db_session
from app.application.services.query_strategy_service import QueryStrategyService

router = APIRouter(prefix="/strategy-templates", tags=["strategy-templates"])

@router.get("")
async def list_templates(request: Request, session: AsyncSession = Depends(get_db_session)):
    result = await QueryStrategyService(session).list_templates()
    return success_response(result, request)

@router.get("/{template_id}")
async def get_template(template_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    result = await QueryStrategyService(session).get_template(template_id)
    return success_response(result, request)
