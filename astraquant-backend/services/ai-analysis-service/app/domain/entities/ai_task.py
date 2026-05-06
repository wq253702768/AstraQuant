from dataclasses import dataclass

@dataclass(frozen=True)
class AiTask:
    id: str
    task_type: str
    related_task_id: str
    status: str
