import hashlib
from app.domain.services.report_filename_builder import ReportFilenameBuilder
from app.infrastructure.minio.minio_client import MinIOClient
from app.infrastructure.postgres.models import ReportFileModel
from app.infrastructure.repositories.report_file_repository import ReportFileRepository
class UploadReportService:
    def __init__(self, session): self.repo=ReportFileRepository(session); self.client=MinIOClient(); self.filename=ReportFilenameBuilder()
    async def upload(self, task, file_format: str, content: str):
        bucket=self.filename.bucket(task.report_type); key=self.filename.object_key(task.report_type, task.related_id, file_format)
        info=self.client.upload_text(bucket,key,content,"text/html" if file_format=="HTML" else "application/json")
        return await self.repo.create(ReportFileModel(report_task_id=task.id, report_type=task.report_type, related_id=task.related_id, file_format=file_format, bucket_name=info["bucket_name"], object_key=info["object_key"], file_url=info["file_url"], file_size=info["file_size"], content_hash=hashlib.sha256(content.encode()).hexdigest()))
