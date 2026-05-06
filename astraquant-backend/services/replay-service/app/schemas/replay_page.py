from pydantic import BaseModel

class BuildReplayRequest(BaseModel):
    backtest_task_id: str
    force_rebuild: bool = False

class BuildReplayResponse(BaseModel):
    replay_build_task_id: str
    status: str
