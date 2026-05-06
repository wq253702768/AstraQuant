from pydantic import BaseModel


class LifecycleDashboardOverview(BaseModel):
    total_strategy_versions: int
    draft_count: int
    backtesting_count: int
    simulation_running_count: int
    simulation_passed_count: int
    small_live_running_count: int
    paused_count: int
    retired_count: int
    pending_approval_count: int
    high_risk_count: int
