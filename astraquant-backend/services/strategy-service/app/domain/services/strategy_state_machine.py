from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus

class StrategyStateMachine:
    allowed_transitions: dict[str, set[str]] = {
        StrategyStatus.DRAFT.value: {StrategyStatus.READY_FOR_BACKTEST.value, StrategyStatus.PAUSED.value, StrategyStatus.RETIRED.value},
        StrategyStatus.READY_FOR_BACKTEST.value: {StrategyStatus.BACKTESTING.value, StrategyStatus.PAUSED.value, StrategyStatus.RETIRED.value},
        StrategyStatus.BACKTESTING.value: {StrategyStatus.PAUSED.value, StrategyStatus.RETIRED.value, StrategyStatus.BACKTEST_FAILED.value, StrategyStatus.BACKTEST_PASSED.value},
        StrategyStatus.BACKTEST_FAILED.value: {StrategyStatus.READY_FOR_BACKTEST.value, StrategyStatus.PAUSED.value, StrategyStatus.RETIRED.value},
        StrategyStatus.BACKTEST_PASSED.value: {StrategyStatus.AI_REVIEWING.value, StrategyStatus.PAUSED.value, StrategyStatus.RETIRED.value},
        StrategyStatus.PAUSED.value: {StrategyStatus.READY_FOR_BACKTEST.value, StrategyStatus.RETIRED.value},
    }

    def can_transition(self, from_status: str, to_status: str) -> bool:
        if from_status == to_status:
            return True
        return to_status in self.allowed_transitions.get(from_status, set())

    def ensure_transition(self, from_status: str, to_status: str) -> None:
        if not self.can_transition(from_status, to_status):
            raise AppError("INVALID_STATE_TRANSITION", f"非法状态流转：{from_status} -> {to_status}", 409)
