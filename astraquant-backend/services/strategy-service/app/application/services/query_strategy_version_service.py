from astra_common.errors import AppError
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy_version import StrategyVersionDetail, StrategyVersionListItem


class QueryStrategyVersionService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)

    async def list_versions(self, strategy_id: str) -> dict:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        versions = await self.version_repo.list_by_strategy(strategy_id)
        items = [
            StrategyVersionListItem(
                id=item.id,
                strategy_id=item.strategy_id,
                version=item.version,
                status=item.status,
                params_hash=item.params_hash,
                created_at=item.created_at.isoformat() if item.created_at else None,
            )
            for item in versions
        ]
        return {"items": items, "total": len(items)}

    async def get_version(self, strategy_id: str, version_id: str) -> StrategyVersionDetail:
        version = await self.version_repo.get(version_id)
        if version is None or version.strategy_id != strategy_id:
            raise AppError("STRATEGY_VERSION_NOT_FOUND", "策略版本不存在", 404)
        return StrategyVersionDetail(
            id=version.id,
            strategy_id=version.strategy_id,
            version=version.version,
            status=version.status,
            params_json=version.params_json,
            risk_params_json=version.risk_params_json,
            params_hash=version.params_hash,
            source_version_id=version.source_version_id,
            created_at=version.created_at.isoformat() if version.created_at else None,
        )
