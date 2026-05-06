from datetime import UTC, datetime
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
from app.schemas.strategy_version import UpdateStrategyParamsRequest, UpdateStrategyParamsResponse
from app.utils.hash_utils import calc_params_hash

class UpdateStrategyParamsService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.validator = StrategyParamValidator()
        self.state_machine = StrategyStateMachine()
        self.publisher = EventPublisher()

    async def execute(self, version_id: str, payload: UpdateStrategyParamsRequest, operator_id: str, trace_id: str | None) -> UpdateStrategyParamsResponse:
        version = await self.version_repo.get(version_id)
        if version is None:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "策略版本不存在", 404)
        if version.status not in {StrategyStatus.DRAFT.value, StrategyStatus.READY_FOR_BACKTEST.value}:
            raise AppError("STRATEGY_VERSION_LOCKED", "当前策略版本已锁定，不能直接修改", 409)
        strategy = await self.strategy_repo.get(version.strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        self.validator.validate(payload.params_json, payload.risk_params_json, version.template.param_schema, version.template.risk_schema)
        old_status = strategy.status
        new_status = StrategyStatus.READY_FOR_BACKTEST.value
        self.state_machine.ensure_transition(old_status, new_status)
        version.params_json = payload.params_json
        version.risk_params_json = payload.risk_params_json
        version.params_hash = calc_params_hash(payload.params_json, payload.risk_params_json)
        version.status = new_status
        strategy.status = new_status
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=version.id, from_status=old_status, to_status=new_status, reason="参数校验通过", operator_id=operator_id))
        now = datetime.now(UTC).isoformat()
        await self.publisher.publish(topics.STRATEGY_STATUS_CHANGED, {"event_type": topics.STRATEGY_STATUS_CHANGED, "strategy_id": strategy.id, "strategy_version_id": version.id, "from_status": old_status, "to_status": new_status, "reason": "参数校验通过", "operator_id": operator_id, "created_at": now})
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "STRATEGY_PARAM_CHANGED", "user_id": operator_id, "resource_type": "strategy_version", "resource_id": version.id, "before": None, "after": {"params_hash": version.params_hash}, "trace_id": trace_id, "created_at": now})
        return UpdateStrategyParamsResponse(strategy_version_id=version.id, status=version.status, params_hash=version.params_hash)
