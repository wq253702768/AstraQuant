from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class SubmitBacktestRequest(BaseModel):
    exchange: str
    symbols: list[str] = Field(min_length=1)
    timeframe: str
    start_time: datetime
    end_time: datetime
    initial_capital: Decimal = Field(gt=0)

class SubmitBacktestResponse(BaseModel):
    task_request_id: str
    status: str
