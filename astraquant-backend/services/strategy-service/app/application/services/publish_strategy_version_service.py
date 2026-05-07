from datetime import UTC, datetime

from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_param_validator import StrategyParamValidator
from app.infrastructure.db.models import StrategyStatusLogModel
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.infrastructure.repositories.strategy_template_repository import StrategyTemplateRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy_version import PublishStrategyVersionResponse
from app.utils.hash_utils import calc_params_hash


class PublishStrategyVersionService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.template_repo = StrategyTemplateRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)
        self.validator = StrategyParamValidator()
        self.publisher = EventPublisher()

    async def execute(self, strategy_id: str, version_id: str, publish_note: str | None, operator_id: str, trace_id: str | None) -> PublishStrategyVersionResponse:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        version = await self.version_repo.get(version_id)
        if version is None or version.strategy_id != strategy_id:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "策略版本不存在", 404)
        if version.status != StrategyStatus.DRAFT.value:
            raise AppError("STRATEGY_VERSION_ALREADY_PUBLISHED", "只有草稿版本可以发布", 409)
        template = await self.template_repo.get(version.template_id)
        if template is None:
            raise AppError("STRATEGY_TEMPLATE_NOT_FOUND", "策略模板不存在或未启用", 404)
        self.validator.validate(version.params_json, version.risk_params_json, template.param_schema, template.risk_schema)
        config_hash = calc_params_hash(version.params_json, version.risk_params_json)
        published_at = datetime.now(UTC)
        version.status = StrategyStatus.PUBLISHED.value
        version.params_hash = config_hash
        version.config_hash = config_hash
        version.published_at = published_at
        version.published_by = operator_id
        await self.strategy_repo.set_latest_version(strategy.id, version.id)
        await self.log_repo.create(
            StrategyStatusLogModel(
                strategy_id=strategy.id,
                strategy_version_id=version.id,
                from_status=StrategyStatus.DRAFT.value,
                to_status=StrategyStatus.PUBLISHED.value,
                reason=publish_note or "发布策略版本",
                operator_id=operator_id,
            )
        )
        now = published_at.isoformat()
        await self.publisher.publish(topics.STRATEGY_STATUS_CHANGED, {"event_type": topics.STRATEGY_STATUS_CHANGED, "strategy_id": strategy.id, "strategy_version_id": version.id, "from_status": "DRAFT", "to_status": "PUBLISHED", "reason": publish_note, "operator_id": operator_id, "created_at": now})
        await self.publisher.publish(topics.AUDIT_EVENT, {"event_type": "STRATEGY_VERSION_PUBLISHED", "user_id": operator_id, "resource_type": "strategy_version", "resource_id": version.id, "after": {"config_hash": config_hash}, "trace_id": trace_id, "created_at": now})
        return PublishStrategyVersionResponse(id=version.id, strategy_id=strategy.id, version=version.version, status=version.status, config_hash=config_hash, published_at=now)
