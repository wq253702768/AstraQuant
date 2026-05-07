from pydantic import BaseModel, Field

class CreateStrategyVersionRequest(BaseModel):
    source_version_id: str | None = None
    change_reason: str = Field(min_length=1)
    params_json: dict | None = None
    risk_params_json: dict | None = None

class CreateStrategyVersionResponse(BaseModel):
    strategy_version_id: str
    version: str
    status: str
    params_hash: str

class UpdateStrategyParamsRequest(BaseModel):
    params_json: dict
    risk_params_json: dict

class UpdateStrategyParamsResponse(BaseModel):
    strategy_version_id: str
    status: str
    params_hash: str

class StrategyVersionListItem(BaseModel):
    id: str
    strategy_id: str
    version: str
    status: str
    params_hash: str
    created_at: str | None = None

class StrategyVersionDetail(BaseModel):
    id: str
    strategy_id: str
    version: str
    status: str
    params_json: dict
    risk_params_json: dict
    params_hash: str
    config_hash: str | None = None
    source_version_id: str | None = None
    published_at: str | None = None
    published_by: str | None = None
    created_at: str | None = None

class PublishStrategyVersionRequest(BaseModel):
    publish_note: str | None = None

class PublishStrategyVersionResponse(BaseModel):
    id: str
    strategy_id: str
    version: str
    status: str
    config_hash: str
    published_at: str

class CopyStrategyVersionRequest(BaseModel):
    change_reason: str = Field(min_length=1)
