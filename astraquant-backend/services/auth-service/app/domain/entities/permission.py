from dataclasses import dataclass

@dataclass(frozen=True)
class Permission:
    id: str
    code: str
    resource: str
    action: str
