from datetime import UTC, datetime
from uuid import uuid4

from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_state_machine import StrategyStateMachine
from app.infrastructure.db.models import StrategyStatusLogModel
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.schemas.strategy import StatusChangeResponse

class PauseStrategyService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.state_machine = StrategyStateMachine()
        self.publisher = EventPublisher()

    async def change_status(self, strategy_id: str, to_status: StrategyStatus, reason: str, operator_id: str, trace_id: str | None) -> StatusChangeResponse:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        old_status = strategy.status
        self.state_machine.ensure_transition(old_status, to_status.value)
        strategy.status = to_status.value
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=None, from_status=old_status, to_status=strategy.status, reason=reason, operator_id=operator_id))
        now = datetime.now(UTC).isoformat()
        await self.publisher.publish(topics.STRATEGY_STATUS_CHANGED, {"event_type": topics.STRATEGY_STATUS_CHANGED, "strategy_id": strategy.id, "strategy_version_id": None, "from_status": old_status, "to_status": strategy.status, "reason": reason, "operator_id": operator_id, "created_at": now})
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "STRATEGY_STATUS_CHANGED", "user_id": operator_id, "resource_type": "strategy", "resource_id": strategy.id, "before": {"status": old_status}, "after": {"status": strategy.status}, "trace_id": trace_id, "created_at": now})
        return StatusChangeResponse(strategy_id=strategy.id, status=strategy.status)
