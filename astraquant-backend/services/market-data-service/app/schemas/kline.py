from datetime import datetime
from pydantic import BaseModel

class KlineResponse(BaseModel):
    ts: datetime
    open: str
    high: str
    low: str
    close: str
    volume: str
    quote_volume: str
