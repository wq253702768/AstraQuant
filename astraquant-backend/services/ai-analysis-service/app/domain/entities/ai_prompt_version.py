from dataclasses import dataclass

@dataclass(frozen=True)
class AiPromptVersion:
    prompt_code: str
    version: str
    agent_name: str
    content: str
