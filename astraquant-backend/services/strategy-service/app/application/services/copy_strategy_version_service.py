from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_version_service import next_version
from app.infrastructure.db.models import StrategyVersionModel
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy_version import CreateStrategyVersionResponse


class CopyStrategyVersionService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)

    async def execute(self, strategy_id: str, version_id: str, change_reason: str, operator_id: str) -> CreateStrategyVersionResponse:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        source = await self.version_repo.get(version_id)
        if source is None or source.strategy_id != strategy_id:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "策略版本不存在", 404)
        versions = await self.version_repo.version_strings(strategy_id)
        version_name = next_version(versions)
        new_version = await self.version_repo.create(
            StrategyVersionModel(
                strategy_id=strategy.id,
                version=version_name,
                template_id=source.template_id,
                params_json=source.params_json,
                risk_params_json=source.risk_params_json,
                params_hash=source.params_hash,
                config_hash=None,
                source_version_id=source.id,
                created_source="copy",
                status=StrategyStatus.DRAFT.value,
                created_by=operator_id,
            )
        )
        await self.strategy_repo.set_latest_version(strategy.id, new_version.id)
        return CreateStrategyVersionResponse(strategy_version_id=new_version.id, version=new_version.version, status=new_version.status, params_hash=new_version.params_hash)
