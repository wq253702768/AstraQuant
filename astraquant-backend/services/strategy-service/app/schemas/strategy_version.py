from pydantic import BaseModel, Field

class CreateStrategyVersionRequest(BaseModel):
    source_version_id: str
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
