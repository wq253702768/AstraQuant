from datetime import UTC, datetime
from uuid import uuid4

from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_param_validator import StrategyParamValidator
from app.domain.services.strategy_state_machine import StrategyStateMachine
from app.domain.services.strategy_version_service import next_version
from app.infrastructure.db.models import StrategyStatusLogModel, StrategyVersionModel
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy_version import CreateStrategyVersionRequest, CreateStrategyVersionResponse
from app.utils.hash_utils import calc_params_hash

class CreateStrategyVersionService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.validator = StrategyParamValidator()
        self.state_machine = StrategyStateMachine()
        self.publisher = EventPublisher()

    async def execute(self, strategy_id: str, payload: CreateStrategyVersionRequest, operator_id: str, trace_id: str | None) -> CreateStrategyVersionResponse:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        source = await self.version_repo.get(payload.source_version_id)
        if source is None or source.strategy_id != strategy_id:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "来源策略版本不存在", 404)
        params = payload.params_json or source.params_json
        risk = payload.risk_params_json or source.risk_params_json
        self.validator.validate(params, risk, source.template.param_schema, source.template.risk_schema)
        versions = await self.version_repo.version_strings(strategy_id)
        version_name = next_version(versions)
        params_hash = calc_params_hash(params, risk)
        version = await self.version_repo.create(StrategyVersionModel(strategy_id=strategy.id, version=version_name, template_id=source.template_id, params_json=params, risk_params_json=risk, params_hash=params_hash, status=StrategyStatus.READY_FOR_BACKTEST.value, created_by=operator_id, created_source="manual", source_version_id=source.id))
        old_status = strategy.status
        self.state_machine.ensure_transition(old_status, StrategyStatus.READY_FOR_BACKTEST.value)
        strategy.status = StrategyStatus.READY_FOR_BACKTEST.value
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=version.id, from_status=old_status, to_status=strategy.status, reason=payload.change_reason, operator_id=operator_id))
        now = datetime.now(UTC).isoformat()
        await self.publisher.publish(topics.STRATEGY_VERSION_CREATED, {"event_type": topics.STRATEGY_VERSION_CREATED, "strategy_id": strategy.id, "strategy_version_id": version.id, "source_version_id": source.id, "operator_id": operator_id, "created_at": now})
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "STRATEGY_VERSION_CREATED", "user_id": operator_id, "resource_type": "strategy", "resource_id": strategy.id, "before": {"source_version_id": source.id}, "after": {"strategy_version_id": version.id}, "trace_id": trace_id, "created_at": now})
        return CreateStrategyVersionResponse(strategy_version_id=version.id, version=version.version, status=version.status, params_hash=version.params_hash)
