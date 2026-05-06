from datetime import datetime
from pydantic import BaseModel, Field
class CreateObservationRequest(BaseModel):
    account_id: str
    strategy_id: str
    strategy_version_id: str
    exchange: str = "OKX"
    symbols: list[str] = Field(min_length=1)
    start_time: datetime
    min_observation_days: int = 7
class ObservationResponse(BaseModel):
    observation_id: str
    status: str
