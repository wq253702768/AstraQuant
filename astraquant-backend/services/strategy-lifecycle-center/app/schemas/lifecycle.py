from pydantic import BaseModel


class InitLifecycleRequest(BaseModel):
    strategy_id: str
    strategy_version_id: str
    created_by: str | None = None


class TransitionRequest(BaseModel):
    to_status: str
    reason: str | None = None


class GateEvaluateRequest(BaseModel):
    gate_code: str

