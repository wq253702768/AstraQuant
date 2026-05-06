from pydantic import BaseModel
class GenerateSignalRequest(BaseModel):
    strategy_id: str
    strategy_version_id: str
    strategy_type: str = "trend_breakout"
    exchange: str = "OKX"
    internal_symbol: str
    params: dict
    snapshot: dict
class SignalResponse(BaseModel):
    signal_id: str | None = None
    status: str
    reason: str | None = None
