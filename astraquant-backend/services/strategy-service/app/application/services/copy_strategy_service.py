from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.infrastructure.db.models import StrategyModel, StrategyVersionModel
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy import CopyStrategyRequest, CreateStrategyResponse


class CopyStrategyService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)

    async def execute(self, strategy_id: str, payload: CopyStrategyRequest, operator_id: str) -> CreateStrategyResponse:
        source = await self.strategy_repo.get(strategy_id)
        if source is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        if await self.strategy_repo.code_exists(payload.code):
            raise AppError("STRATEGY_CODE_ALREADY_EXISTS", "策略编码已存在", 409)
        strategy = await self.strategy_repo.create(
            StrategyModel(
                name=payload.name,
                code=payload.code,
                strategy_type=source.strategy_type,
                description=source.description,
                status=StrategyStatus.ACTIVE.value,
                tags=source.tags,
                created_by=operator_id,
            )
        )
        source_version = await self.strategy_repo.latest_version(source.id)
        if source_version is None:
            return CreateStrategyResponse(id=strategy.id, strategy_id=strategy.id, strategy_version_id="", name=strategy.name, code=strategy.code, status=strategy.status)
        version = await self.version_repo.create(
            StrategyVersionModel(
                strategy_id=strategy.id,
                version="v1.0",
                template_id=source_version.template_id,
                params_json=source_version.params_json,
                risk_params_json=source_version.risk_params_json,
                params_hash=source_version.params_hash,
                code_hash=source_version.code_hash,
                source_version_id=source_version.id,
                created_source="copy",
                status=StrategyStatus.DRAFT.value,
                created_by=operator_id,
            )
        )
        await self.strategy_repo.set_latest_version(strategy.id, version.id)
        return CreateStrategyResponse(id=strategy.id, strategy_id=strategy.id, strategy_version_id=version.id, name=strategy.name, code=strategy.code, status=strategy.status)
