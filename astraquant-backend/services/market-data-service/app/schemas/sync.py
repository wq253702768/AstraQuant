from datetime import datetime
from pydantic import BaseModel, Field

class CreateSyncTaskRequest(BaseModel):
    exchange: str
    symbols: list[str] = Field(min_length=1)
    data_types: list[str] = Field(min_length=1)
    timeframes: list[str] | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    force_resync: bool = False

class CreateSyncTaskResponse(BaseModel):
    sync_task_id: str
    status: str

class SyncTaskStatusResponse(BaseModel):
    sync_task_id: str
    status: str
    progress: float
    current_stage: str | None = None
    error_message: str | None = None
