from dataclasses import dataclass

@dataclass(frozen=True)
class Role:
    id: str
    code: str
    name: str
