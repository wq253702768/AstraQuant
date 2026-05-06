from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_report_task_service import CreateReportTaskService
from app.application.services.query_report_service import QueryReportService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.report import CreateReportTaskRequest
router=APIRouter(prefix="/reports", tags=["reports"])
@router.post("/build")
async def build(payload: CreateReportTaskRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await CreateReportTaskService(session).execute(payload, operator_id); await session.commit(); return success_response(result, request)
@router.get("/tasks/{report_task_id}")
async def task(report_task_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    return success_response(await QueryReportService(session).task(report_task_id), request)
@router.get("/tasks/{report_task_id}/files")
async def files(report_task_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    return success_response(await QueryReportService(session).files(report_task_id), request)
