from datetime import datetime
from pydantic import BaseModel

class MarkPriceResponse(BaseModel):
    exchange: str
    symbol: str
    mark_price: str
    index_price: str | None = None
    ts: datetime
