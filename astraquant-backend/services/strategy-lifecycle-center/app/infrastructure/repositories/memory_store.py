from dataclasses import asdict

from app.domain.entities.lifecycle import (
    LifecycleApproval,
    LifecycleEvent,
    LifecycleEvidence,
    LifecycleStageGateResult,
    LifecycleTask,
    StrategyLifecycleState,
)


class LifecycleMemoryStore:
    def __init__(self) -> None:
        self.states: dict[str, StrategyLifecycleState] = {}
        self.events: list[LifecycleEvent] = []
        self.evidence: list[LifecycleEvidence] = []
        self.approvals: dict[str, LifecycleApproval] = {}
        self.tasks: list[LifecycleTask] = []
        self.gate_results: list[LifecycleStageGateResult] = []

    def reset(self) -> None:
        self.__init__()

    def upsert_state(self, state: StrategyLifecycleState) -> StrategyLifecycleState:
        self.states[state.strategy_version_id] = state
        return state

    def get_state(self, strategy_version_id: str) -> StrategyLifecycleState | None:
        return self.states.get(strategy_version_id)

    def list_states(self, filters: dict) -> list[StrategyLifecycleState]:
        items = list(self.states.values())
        for key in ("current_status", "current_stage", "strategy_id", "strategy_version_id"):
            if filters.get(key):
                items = [item for item in items if getattr(item, key) == filters[key]]
        if filters.get("live_enabled") is not None:
            items = [item for item in items if item.live_enabled is filters["live_enabled"]]
        if filters.get("retired") is not None:
            items = [item for item in items if item.retired is filters["retired"]]
        return sorted(items, key=lambda item: item.updated_at, reverse=True)

    def add_event(self, event: LifecycleEvent) -> LifecycleEvent:
        self.events.append(event)
        return event

    def add_evidence(self, evidence: LifecycleEvidence) -> LifecycleEvidence:
        self.evidence.append(evidence)
        return evidence

    def list_evidence(self, strategy_version_id: str) -> list[LifecycleEvidence]:
        return [item for item in self.evidence if item.strategy_version_id == strategy_version_id]

    def add_approval(self, approval: LifecycleApproval) -> LifecycleApproval:
        self.approvals[approval.id] = approval
        return approval

    def get_approval(self, approval_id: str) -> LifecycleApproval | None:
        return self.approvals.get(approval_id)

    def pending_approval(self, strategy_version_id: str, approval_type: str) -> LifecycleApproval | None:
        for approval in self.approvals.values():
            if approval.strategy_version_id == strategy_version_id and approval.approval_type == approval_type and approval.approval_status == "PENDING":
                return approval
        return None

    def add_task(self, task: LifecycleTask) -> LifecycleTask:
        self.tasks.append(task)
        return task

    def add_gate_result(self, gate_result: LifecycleStageGateResult) -> LifecycleStageGateResult:
        self.gate_results.append(gate_result)
        return gate_result

    def list_events(self, strategy_version_id: str) -> list[LifecycleEvent]:
        return [item for item in self.events if item.strategy_version_id == strategy_version_id]

    def dashboard(self) -> dict:
        states = list(self.states.values())
        pending = [item for item in self.approvals.values() if item.approval_status == "PENDING"]
        high_risk = [item for item in states if item.risk_level in {"HIGH", "CRITICAL"}]
        return {
            "total_strategy_versions": len(states),
            "draft_count": sum(item.current_status == "DRAFT" for item in states),
            "backtesting_count": sum(item.current_status == "BACKTESTING" for item in states),
            "simulation_running_count": sum(item.current_status == "SIMULATION_RUNNING" for item in states),
            "simulation_passed_count": sum(item.current_status == "SIMULATION_ADMISSION_PASSED" for item in states),
            "small_live_running_count": sum(item.current_status == "SMALL_LIVE_RUNNING" for item in states),
            "paused_count": sum(item.current_status == "PAUSED" for item in states),
            "retired_count": sum(item.retired for item in states),
            "pending_approval_count": len(pending),
            "high_risk_count": len(high_risk),
        }

    @staticmethod
    def to_dict(entity) -> dict:
        data = asdict(entity)
        for key, value in list(data.items()):
            if hasattr(value, "isoformat"):
                data[key] = value.isoformat()
        return data


store = LifecycleMemoryStore()
