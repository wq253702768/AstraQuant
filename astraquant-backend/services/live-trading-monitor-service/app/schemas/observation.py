from datetime import datetime
from pydantic import BaseModel, Field
class CreateLiveObservationRequest(BaseModel):
    account_id: str
    strategy_id: str
    strategy_version_id: str
    exchange: str = "OKX"
    symbols: list[str] = Field(min_length=1)
    observation_type: str = "SMALL_LIVE_OBSERVATION"
    start_time: datetime
    min_observation_days: int = 7
class LiveObservationResponse(BaseModel):
    live_observation_id: str
    status: str
