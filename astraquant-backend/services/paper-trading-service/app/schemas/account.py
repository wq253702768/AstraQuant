from decimal import Decimal
from pydantic import BaseModel, Field
class CreatePaperAccountRequest(BaseModel):
    name: str
    exchange: str = "OKX"
    currency: str = "USDT"
    initial_balance: Decimal = Field(gt=0)
class PaperAccountResponse(BaseModel):
    account_id: str
    name: str
    initial_balance: str
    equity: str
    status: str
