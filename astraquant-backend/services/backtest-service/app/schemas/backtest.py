from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class CreateBacktestRequest(BaseModel):
    strategy_version_id: str
    exchange: str
    symbols: list[str] = Field(min_length=1)
    timeframe: str
    start_time: datetime
    end_time: datetime
    initial_capital: Decimal = Field(gt=0)
    cost_model: dict
    risk_model: dict

class CreateBacktestResponse(BaseModel):
    task_id: str
    status: str

class BacktestStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: float
    current_stage: str | None = None
    processed_bars: int = 0
    total_bars: int = 0
    error_message: str | None = None

class BacktestSummaryResponse(BaseModel):
    task_id: str
    total_return: str | None = None
    annual_return: str | None = None
    final_equity: str | None = None
    max_drawdown: str | None = None
    win_rate: str | None = None
    profit_loss_ratio: str | None = None
    profit_factor: str | None = None
    trade_count: int | None = None
    max_consecutive_losses: int | None = None
    fee_total: str | None = None
    slippage_total: str | None = None
    funding_fee_total: str | None = None
    net_profit: str | None = None
    decision: str | None = None
