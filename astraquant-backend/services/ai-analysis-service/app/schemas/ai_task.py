from pydantic import BaseModel, Field

class CreateAIBacktestAnalysisRequest(BaseModel):
    backtest_task_id: str
    analysis_type: str = "FULL_BACKTEST_REVIEW"
    agents: list[str] = Field(default_factory=list)

class CreateAIBacktestAnalysisResponse(BaseModel):
    ai_task_id: str
    status: str

class AITaskStatusResponse(BaseModel):
    ai_task_id: str
    status: str
    current_agent: str | None = None
    progress: float
    error_message: str | None = None
