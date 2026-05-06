from dataclasses import dataclass
from datetime import datetime

@dataclass
class Strategy:
    id: str
    name: str
    code: str
    strategy_type: str
    description: str | None
    status: str
    tags: dict | None
    created_by: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
