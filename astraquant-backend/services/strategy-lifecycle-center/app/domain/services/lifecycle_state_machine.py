from astra_common.errors import AppError
from app.domain.enums.lifecycle_stage import LifecycleStage
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


TERMINAL_SAFE_STATUSES = {
    StrategyLifecycleStatus.PAUSED,
    StrategyLifecycleStatus.ROLLBACK_TO_PAPER,
    StrategyLifecycleStatus.RETEST_REQUIRED,
    StrategyLifecycleStatus.REVIEW_REQUIRED,
    StrategyLifecycleStatus.RETIRED,
}


class LifecycleStateMachine:
    def __init__(self) -> None:
        self.transitions: dict[StrategyLifecycleStatus, set[StrategyLifecycleStatus]] = {
            StrategyLifecycleStatus.DRAFT: {StrategyLifecycleStatus.BACKTESTING, StrategyLifecycleStatus.BACKTEST_COMPLETED, StrategyLifecycleStatus.RETIRED},
            StrategyLifecycleStatus.BACKTESTING: {StrategyLifecycleStatus.BACKTEST_COMPLETED, StrategyLifecycleStatus.BACKTEST_FAILED, StrategyLifecycleStatus.RETEST_REQUIRED},
            StrategyLifecycleStatus.BACKTEST_COMPLETED: {StrategyLifecycleStatus.AI_REVIEWING, StrategyLifecycleStatus.RETEST_REQUIRED},
            StrategyLifecycleStatus.BACKTEST_FAILED: {StrategyLifecycleStatus.RETEST_REQUIRED, StrategyLifecycleStatus.BACKTESTING},
            StrategyLifecycleStatus.AI_REVIEWING: {StrategyLifecycleStatus.AI_REVIEW_COMPLETED, StrategyLifecycleStatus.REVIEW_REQUIRED},
            StrategyLifecycleStatus.AI_REVIEW_COMPLETED: {StrategyLifecycleStatus.SCORING},
            StrategyLifecycleStatus.SCORING: {StrategyLifecycleStatus.SCORE_COMPLETED, StrategyLifecycleStatus.SCORE_REJECTED},
            StrategyLifecycleStatus.SCORE_COMPLETED: {StrategyLifecycleStatus.SIMULATION_READY, StrategyLifecycleStatus.SCORE_REJECTED, StrategyLifecycleStatus.RETEST_REQUIRED},
            StrategyLifecycleStatus.SCORE_REJECTED: {StrategyLifecycleStatus.RETEST_REQUIRED, StrategyLifecycleStatus.BACKTESTING},
            StrategyLifecycleStatus.SIMULATION_READY: {StrategyLifecycleStatus.SIMULATION_RUNNING},
            StrategyLifecycleStatus.SIMULATION_RUNNING: {StrategyLifecycleStatus.SIMULATION_COMPLETED, StrategyLifecycleStatus.SIMULATION_REJECTED},
            StrategyLifecycleStatus.SIMULATION_COMPLETED: {StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED, StrategyLifecycleStatus.SIMULATION_REJECTED, StrategyLifecycleStatus.RETEST_REQUIRED},
            StrategyLifecycleStatus.SIMULATION_REJECTED: {StrategyLifecycleStatus.RETEST_REQUIRED, StrategyLifecycleStatus.SIMULATION_RUNNING},
            StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED: {StrategyLifecycleStatus.SMALL_LIVE_APPLICATION_PENDING, StrategyLifecycleStatus.ROLLBACK_TO_PAPER},
            StrategyLifecycleStatus.SMALL_LIVE_APPLICATION_PENDING: {StrategyLifecycleStatus.SMALL_LIVE_APPROVED, StrategyLifecycleStatus.SMALL_LIVE_REJECTED},
            StrategyLifecycleStatus.SMALL_LIVE_APPROVED: {StrategyLifecycleStatus.SMALL_LIVE_RUNNING},
            StrategyLifecycleStatus.SMALL_LIVE_REJECTED: {StrategyLifecycleStatus.SIMULATION_ADMISSION_PASSED, StrategyLifecycleStatus.REVIEW_REQUIRED},
            StrategyLifecycleStatus.SMALL_LIVE_RUNNING: {StrategyLifecycleStatus.SMALL_LIVE_COMPLETED, StrategyLifecycleStatus.SMALL_LIVE_PAUSED, StrategyLifecycleStatus.ROLLBACK_TO_PAPER, StrategyLifecycleStatus.PAUSED},
            StrategyLifecycleStatus.SMALL_LIVE_PAUSED: {StrategyLifecycleStatus.REVIEW_REQUIRED, StrategyLifecycleStatus.ROLLBACK_TO_PAPER},
            StrategyLifecycleStatus.SMALL_LIVE_COMPLETED: {StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED, StrategyLifecycleStatus.ROLLBACK_TO_PAPER, StrategyLifecycleStatus.PAUSED},
            StrategyLifecycleStatus.LIVE_REVIEW_COMPLETED: {StrategyLifecycleStatus.SCALE_UP_APPLICATION_PENDING, StrategyLifecycleStatus.SMALL_LIVE_RUNNING, StrategyLifecycleStatus.ROLLBACK_TO_PAPER, StrategyLifecycleStatus.PAUSED},
            StrategyLifecycleStatus.SCALE_UP_APPLICATION_PENDING: {StrategyLifecycleStatus.SCALE_UP_APPROVED, StrategyLifecycleStatus.SCALE_UP_REJECTED},
            StrategyLifecycleStatus.SCALE_UP_APPROVED: {StrategyLifecycleStatus.SMALL_LIVE_RUNNING, StrategyLifecycleStatus.PAUSED},
            StrategyLifecycleStatus.SCALE_UP_REJECTED: {StrategyLifecycleStatus.SMALL_LIVE_RUNNING, StrategyLifecycleStatus.REVIEW_REQUIRED},
            StrategyLifecycleStatus.ROLLBACK_TO_PAPER: {StrategyLifecycleStatus.SIMULATION_RUNNING, StrategyLifecycleStatus.RETEST_REQUIRED, StrategyLifecycleStatus.RETIRED},
            StrategyLifecycleStatus.RETEST_REQUIRED: {StrategyLifecycleStatus.BACKTESTING, StrategyLifecycleStatus.RETIRED},
            StrategyLifecycleStatus.PAUSED: {StrategyLifecycleStatus.REVIEW_REQUIRED, StrategyLifecycleStatus.ROLLBACK_TO_PAPER, StrategyLifecycleStatus.RETIRED},
            StrategyLifecycleStatus.REVIEW_REQUIRED: {StrategyLifecycleStatus.BACKTESTING, StrategyLifecycleStatus.SIMULATION_RUNNING, StrategyLifecycleStatus.RETIRED},
            StrategyLifecycleStatus.RETIRED: set(),
        }

    def ensure_can_transition(self, from_status: StrategyLifecycleStatus | str, to_status: StrategyLifecycleStatus | str) -> None:
        source = StrategyLifecycleStatus(from_status)
        target = StrategyLifecycleStatus(to_status)
        if target in TERMINAL_SAFE_STATUSES and source != StrategyLifecycleStatus.RETIRED:
            return
        if target not in self.transitions[source]:
            raise AppError("INVALID_LIFECYCLE_TRANSITION", f"生命周期状态不允许从 {source} 流转到 {target}", 409)

    def stage_for_status(self, status: StrategyLifecycleStatus | str) -> LifecycleStage:
        value = StrategyLifecycleStatus(status)
        if value in {StrategyLifecycleStatus.DRAFT}:
            return LifecycleStage.DRAFT
        if value.name.startswith("BACKTEST") or value == StrategyLifecycleStatus.RETEST_REQUIRED:
            return LifecycleStage.BACKTEST
        if value.name.startswith("AI_"):
            return LifecycleStage.AI_REVIEW
        if value.name.startswith("SCORE"):
            return LifecycleStage.SCORING
        if value.name.startswith("SIMULATION") or value == StrategyLifecycleStatus.ROLLBACK_TO_PAPER:
            return LifecycleStage.SIMULATION
        if value.name.startswith("SMALL_LIVE") or value.name.startswith("LIVE_") or value.name.startswith("SCALE_UP"):
            return LifecycleStage.LIVE
        if value == StrategyLifecycleStatus.RETIRED:
            return LifecycleStage.RETIRED
        return LifecycleStage.GOVERNANCE
