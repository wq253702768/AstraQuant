from datetime import datetime
from pydantic import BaseModel, Field

class CreateStrategyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    code: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_\-]+$")
    strategy_type: str
    template_id: str
    description: str | None = None
    tags: dict | None = None

class CreateStrategyResponse(BaseModel):
    strategy_id: str
    strategy_version_id: str
    status: str

class StrategyListItem(BaseModel):
    id: str
    name: str
    code: str
    strategy_type: str
    status: str
    latest_version: str | None = None
    created_at: datetime | None = None

class StrategyVersionSummary(BaseModel):
    id: str
    version: str
    status: str
    params_hash: str
    created_at: datetime | None = None

class StrategyDetail(BaseModel):
    id: str
    name: str
    code: str
    strategy_type: str
    status: str
    description: str | None = None
    versions: list[StrategyVersionSummary]

class StatusChangeRequest(BaseModel):
    reason: str = Field(min_length=1)

class StatusChangeResponse(BaseModel):
    strategy_id: str
    status: str
