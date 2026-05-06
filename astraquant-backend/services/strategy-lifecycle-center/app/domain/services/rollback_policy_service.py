from app.domain.entities.lifecycle import StrategyLifecycleState, utcnow
from app.domain.enums.lifecycle_stage import LifecycleStage
from app.domain.enums.lifecycle_status import StrategyLifecycleStatus


class RollbackPolicyService:
    def rollback_to_paper(self, state: StrategyLifecycleState, reason: str) -> StrategyLifecycleState:
        state.current_status = StrategyLifecycleStatus.ROLLBACK_TO_PAPER.value
        state.current_stage = LifecycleStage.SIMULATION.value
        state.live_enabled = False
        state.scale_up_allowed = False
        state.latest_gate_reason = reason
        state.updated_at = utcnow()
        return state

    def pause(self, state: StrategyLifecycleState, reason: str) -> StrategyLifecycleState:
        state.current_status = StrategyLifecycleStatus.PAUSED.value
        state.current_stage = LifecycleStage.GOVERNANCE.value
        state.live_enabled = False
        state.scale_up_allowed = False
        state.latest_gate_reason = reason
        state.updated_at = utcnow()
        return state

    def retire(self, state: StrategyLifecycleState, reason: str) -> StrategyLifecycleState:
        state.current_status = StrategyLifecycleStatus.RETIRED.value
        state.current_stage = LifecycleStage.RETIRED.value
        state.live_enabled = False
        state.scale_up_allowed = False
        state.retired = True
        state.latest_gate_reason = reason
        state.updated_at = utcnow()
        return state

    def target_for_failure(self, failure_source: str) -> StrategyLifecycleStatus:
        if failure_source in {"LIVE_MONITOR", "ORDER_EXECUTOR", "LIVE_RISK_GUARD"}:
            return StrategyLifecycleStatus.ROLLBACK_TO_PAPER
        if failure_source in {"PAPER_MONITOR", "SCORE"}:
            return StrategyLifecycleStatus.RETEST_REQUIRED
        return StrategyLifecycleStatus.REVIEW_REQUIRED
