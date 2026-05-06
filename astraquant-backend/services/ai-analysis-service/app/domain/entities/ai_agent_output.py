from dataclasses import dataclass

@dataclass(frozen=True)
class AiAgentOutput:
    ai_task_id: str
    agent_name: str
    output_json: dict
