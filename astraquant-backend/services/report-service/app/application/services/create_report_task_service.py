from app.domain.enums.report_status import ReportStatus
from app.infrastructure.postgres.models import ReportTaskModel
from app.infrastructure.repositories.report_task_repository import ReportTaskRepository
from app.schemas.report import CreateReportTaskRequest, CreateReportTaskResponse
class CreateReportTaskService:
    def __init__(self, session): self.repo=ReportTaskRepository(session)
    async def execute(self, payload: CreateReportTaskRequest, operator_id: str | None):
        task=await self.repo.create(ReportTaskModel(report_type=payload.report_type, related_id=payload.related_id, formats=payload.formats, status=ReportStatus.QUEUED.value, progress=0, current_stage="queued", created_by=operator_id))
        return CreateReportTaskResponse(report_task_id=task.id, status=task.status)
