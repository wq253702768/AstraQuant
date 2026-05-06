from pydantic import BaseModel, Field
class CreateReportTaskRequest(BaseModel):
    report_type: str
    related_id: str
    formats: list[str] = Field(default_factory=lambda: ["HTML", "JSON"])
class CreateReportTaskResponse(BaseModel):
    report_task_id: str
    status: str
