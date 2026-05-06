from dataclasses import dataclass

@dataclass(frozen=True)
class AgentResult:
    agent_name: str
    output: dict

class BaseAgent:
    agent_name = "base_agent"
    def run(self, input_data: dict, previous_outputs: dict | None = None) -> dict:
        raise NotImplementedError
