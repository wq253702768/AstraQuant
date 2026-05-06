from pydantic import BaseModel
class CreateExchangeAccountRequest(BaseModel):
    name: str
    exchange: str = "OKX"
    account_type: str = "MAIN"
    environment: str = "PROD"
    default_currency: str = "USDT"
    expected_outbound_ip: str | None = None
class ExchangeAccountResponse(BaseModel):
    account_id: str
    status: str
