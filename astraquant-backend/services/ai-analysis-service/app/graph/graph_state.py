from typing import TypedDict

class BacktestReviewState(TypedDict, total=False):
    ai_task_id: str
    backtest_task_id: str
    input_data: dict
    input_data_hash: str
    data_validation_output: dict | None
    strategy_performance_output: dict | None
    drawdown_attribution_output: dict | None
    cost_analyzer_output: dict | None
    parameter_optimizer_output: dict | None
    risk_reviewer_output: dict | None
    opponent_reviewer_output: dict | None
    summary_output: dict | None
    errors: list[str]
