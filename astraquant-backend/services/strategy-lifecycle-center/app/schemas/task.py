from pydantic import BaseModel


class LifecycleTaskResponse(BaseModel):
    task_id: str
    task_type: str
    task_status: str
    title: str
