from datetime import UTC, datetime
from uuid import uuid4

from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_template_service import DEFAULT_RISK_PARAMS
from app.infrastructure.db.models import StrategyModel, StrategyStatusLogModel, StrategyVersionModel
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.infrastructure.repositories.strategy_template_repository import StrategyTemplateRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy import CreateStrategyRequest, CreateStrategyResponse
from app.utils.hash_utils import calc_params_hash

class CreateStrategyService:
    def __init__(self, session):
        self.session = session
        self.strategy_repo = StrategyRepository(session)
        self.template_repo = StrategyTemplateRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.publisher = EventPublisher()

    async def execute(self, payload: CreateStrategyRequest, operator_id: str, trace_id: str | None) -> CreateStrategyResponse:
        template = await self.template_repo.get(payload.template_id)
        if template is None or not template.enabled:
            raise AppError("STRATEGY_TEMPLATE_NOT_FOUND", "策略模板不存在或未启用", 404)
        if await self.strategy_repo.code_exists(payload.code):
            raise AppError("STRATEGY_CODE_EXISTS", "策略编码已存在", 409)
        strategy = await self.strategy_repo.create(StrategyModel(name=payload.name, code=payload.code, strategy_type=payload.strategy_type, description=payload.description, status=StrategyStatus.DRAFT.value, tags=payload.tags, created_by=operator_id))
        params_hash = calc_params_hash(template.default_params, DEFAULT_RISK_PARAMS)
        version = await self.version_repo.create(StrategyVersionModel(strategy_id=strategy.id, version="v1.0", template_id=template.id, params_json=template.default_params, risk_params_json=DEFAULT_RISK_PARAMS, params_hash=params_hash, status=StrategyStatus.DRAFT.value, created_by=operator_id, created_source="manual"))
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=version.id, from_status=None, to_status=StrategyStatus.DRAFT.value, reason="创建策略", operator_id=operator_id))
        now = datetime.now(UTC).isoformat()
        await self.publisher.publish(topics.STRATEGY_CREATED, {"event_type": topics.STRATEGY_CREATED, "strategy_id": strategy.id, "strategy_version_id": version.id, "operator_id": operator_id, "created_at": now})
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "STRATEGY_CREATED", "user_id": operator_id, "resource_type": "strategy", "resource_id": strategy.id, "before": None, "after": {"code": strategy.code}, "trace_id": trace_id, "created_at": now})
        return CreateStrategyResponse(strategy_id=strategy.id, strategy_version_id=version.id, status=strategy.status)
