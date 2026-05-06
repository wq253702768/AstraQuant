from app.domain.services.stage_gate_engine import StageGateEngine


class BaseGate:
    gate_code: str

    def __init__(self) -> None:
        self.engine = StageGateEngine()

    def evaluate(self, state, evidence):
        return self.engine.evaluate(self.gate_code, state, evidence)
