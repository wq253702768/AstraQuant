from datetime import datetime
from pydantic import BaseModel

class FundingRateResponse(BaseModel):
    exchange: str
    symbol: str
    funding_rate: str
    realized_rate: str | None = None
    funding_time: datetime
    next_funding_time: datetime | None = None
    mark_price: str
