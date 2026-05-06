from app.domain.enums.report_status import ReportStatus
from app.domain.services.report_payload_builder import ReportPayloadBuilder
from app.infrastructure.repositories.report_task_repository import ReportTaskRepository
from app.renderers.html_renderer import HTMLRenderer
from app.renderers.json_renderer import JSONRenderer
from app.application.services.upload_report_service import UploadReportService
class BuildReportService:
    def __init__(self, session): self.task_repo=ReportTaskRepository(session); self.uploader=UploadReportService(session)
    async def build(self, task_id: str):
        task=await self.task_repo.get(task_id)
        if not task: return None
        task.status=ReportStatus.RUNNING.value; task.current_stage="rendering"
        payload=ReportPayloadBuilder().build(task.report_type, task.related_id)
        if "HTML" in task.formats: await self.uploader.upload(task,"HTML",HTMLRenderer().render(task.report_type,payload))
        if "JSON" in task.formats: await self.uploader.upload(task,"JSON",JSONRenderer().render(payload))
        task.status=ReportStatus.COMPLETED.value; task.progress=100; task.current_stage="completed"
        return task
