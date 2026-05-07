from datetime import datetime
from pydantic import BaseModel, Field

class CreateStrategyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    code: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_\-]+$")
    strategy_type: str = "CONFIG"
    template_id: str | None = None
    description: str | None = None
    tags: list[str] | dict | None = None

class CreateStrategyResponse(BaseModel):
    id: str
    strategy_id: str
    strategy_version_id: str
    name: str
    code: str
    status: str

class UpdateStrategyRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    tags: list[str] | dict | None = None

class CopyStrategyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    code: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_\-]+$")

class StrategyListItem(BaseModel):
    id: str
    name: str
    code: str
    strategy_type: str
    status: str
    tags: list[str] | dict | None = None
    latest_version: str | None = None
    latest_version_id: str | None = None
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
    tags: list[str] | dict | None = None
    latest_version_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    versions: list[StrategyVersionSummary]

class StatusChangeRequest(BaseModel):
    reason: str = Field(min_length=1)

class StatusChangeResponse(BaseModel):
    strategy_id: str
    status: str
