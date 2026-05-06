from dataclasses import dataclass

@dataclass(frozen=True)
class AiModelCallLog:
    ai_task_id: str
    agent_name: str
    model_name: str
