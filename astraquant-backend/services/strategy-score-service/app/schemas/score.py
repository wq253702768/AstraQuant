from pydantic import BaseModel

class CalculateScoreRequest(BaseModel):
    strategy_version_id: str
    backtest_task_id: str
    ai_task_id: str | None = None

class CalculateScoreResponse(BaseModel):
    score_id: str
    total_score: float
    grade: str
    decision: str
