from astra_common.errors import AppError
from app.infrastructure.repositories.report_file_repository import ReportFileRepository
from app.infrastructure.repositories.report_task_repository import ReportTaskRepository
class QueryReportService:
    def __init__(self, session): self.task_repo=ReportTaskRepository(session); self.file_repo=ReportFileRepository(session)
    async def task(self, task_id: str):
        task=await self.task_repo.get(task_id)
        if not task: raise AppError("REPORT_TASK_NOT_FOUND","报告任务不存在",404)
        return {"report_task_id":task.id,"status":task.status,"progress":float(task.progress),"current_stage":task.current_stage}
    async def files(self, task_id: str):
        files=await self.file_repo.list_by_task(task_id)
        return {"items":[{"report_file_id":f.id,"report_type":f.report_type,"file_format":f.file_format,"file_url":f.file_url,"file_size":f.file_size,"created_at":f.created_at} for f in files]}
