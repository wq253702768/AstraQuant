from datetime import UTC, datetime
from uuid import uuid4

from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_param_validator import StrategyParamValidator
from app.domain.services.strategy_state_machine import StrategyStateMachine
from app.infrastructure.db.models import StrategyStatusLogModel
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.backtest_submit import SubmitBacktestRequest, SubmitBacktestResponse

class SubmitBacktestService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.validator = StrategyParamValidator()
        self.state_machine = StrategyStateMachine()
        self.publisher = EventPublisher()

    async def execute(self, version_id: str, payload: SubmitBacktestRequest, operator_id: str, trace_id: str | None) -> SubmitBacktestResponse:
        version = await self.version_repo.get(version_id)
        if version is None:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "策略版本不存在", 404)
        strategy = await self.strategy_repo.get(version.strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        if version.status != StrategyStatus.READY_FOR_BACKTEST.value:
            raise AppError("BACKTEST_SUBMIT_NOT_ALLOWED", "策略版本未准备好，不能提交回测", 409)
        self.validator.validate(version.params_json, version.risk_params_json, version.template.param_schema, version.template.risk_schema)
        old_status = strategy.status
        self.state_machine.ensure_transition(old_status, StrategyStatus.BACKTESTING.value)
        strategy.status = StrategyStatus.BACKTESTING.value
        version.status = StrategyStatus.BACKTESTING.value
        task_request_id = f"bt_req_{uuid4().hex}"
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=version.id, from_status=old_status, to_status=strategy.status, reason="提交回测", operator_id=operator_id))
        now = datetime.now(UTC).isoformat()
        event = {"event_type": topics.BACKTEST_TASK_CREATED, "task_request_id": task_request_id, "strategy_id": strategy.id, "strategy_version_id": version.id, "exchange": payload.exchange, "symbols": payload.symbols, "timeframe": payload.timeframe, "start_time": payload.start_time.isoformat(), "end_time": payload.end_time.isoformat(), "initial_capital": str(payload.initial_capital), "params_hash": version.params_hash, "created_at": now}
        await self.publisher.publish(topics.BACKTEST_TASK_CREATED, event)
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "BACKTEST_SUBMITTED", "user_id": operator_id, "resource_type": "strategy_version", "resource_id": version.id, "before": {"status": old_status}, "after": {"status": strategy.status, "task_request_id": task_request_id}, "trace_id": trace_id, "created_at": now})
        return SubmitBacktestResponse(task_request_id=task_request_id, status=strategy.status)
