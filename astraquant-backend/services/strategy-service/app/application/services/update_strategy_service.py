from astra_common.errors import AppError
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.schemas.strategy import StrategyDetail, StrategyVersionSummary, UpdateStrategyRequest
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository


class UpdateStrategyService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)

    async def execute(self, strategy_id: str, payload: UpdateStrategyRequest, operator_id: str) -> StrategyDetail:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        if strategy.status == "ARCHIVED":
            raise AppError("STRATEGY_ARCHIVED", "策略已归档", 409)
        strategy = await self.strategy_repo.update_basic(strategy, payload.name, payload.description, payload.tags, operator_id)
        versions = await self.version_repo.list_by_strategy(strategy_id)
        return StrategyDetail(
            id=strategy.id,
            name=strategy.name,
            code=strategy.code,
            strategy_type=strategy.strategy_type,
            status=strategy.status,
            description=strategy.description,
            tags=strategy.tags,
            latest_version_id=strategy.latest_version_id,
            created_at=strategy.created_at,
            updated_at=strategy.updated_at,
            versions=[StrategyVersionSummary(id=item.id, version=item.version, status=item.status, params_hash=item.params_hash, created_at=item.created_at) for item in versions],
        )
