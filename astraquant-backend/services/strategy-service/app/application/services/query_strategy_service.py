from astra_common.errors import AppError
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_template_repository import StrategyTemplateRepository
from app.infrastructure.repositories.strategy_version_repository import StrategyVersionRepository
from app.schemas.strategy import StrategyDetail, StrategyListItem, StrategyVersionSummary
from app.schemas.strategy_template import StrategyTemplateDetail, StrategyTemplateListItem

class QueryStrategyService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.version_repo = StrategyVersionRepository(session)
        self.template_repo = StrategyTemplateRepository(session)

    async def list_templates(self) -> dict:
        items = [StrategyTemplateListItem(id=item.id, code=item.code, name=item.name, strategy_type=item.strategy_type, description=item.description, default_config=item.default_config or item.default_params) for item in await self.template_repo.list_enabled()]
        return {"items": items, "total": len(items)}

    async def get_template(self, template_id: str) -> StrategyTemplateDetail:
        item = await self.template_repo.get(template_id)
        if item is None:
            raise AppError("STRATEGY_TEMPLATE_NOT_FOUND", "策略模板不存在", 404)
        return StrategyTemplateDetail(id=item.id, code=item.code, name=item.name, strategy_type=item.strategy_type, description=item.description, default_params=item.default_params, default_config=item.default_config or item.default_params, param_schema=item.param_schema, risk_schema=item.risk_schema)

    async def list_strategies(self, status: str | None, strategy_type: str | None, keyword: str | None, page: int, page_size: int) -> dict:
        strategies, total = await self.strategy_repo.list(status, strategy_type, keyword, page, page_size)
        items = []
        for strategy in strategies:
            latest = await self.strategy_repo.latest_version(strategy.id)
            items.append(StrategyListItem(id=strategy.id, name=strategy.name, code=strategy.code, strategy_type=strategy.strategy_type, status=strategy.status, tags=strategy.tags, latest_version=latest.version if latest else None, latest_version_id=latest.id if latest else strategy.latest_version_id, created_at=strategy.created_at))
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_strategy(self, strategy_id: str) -> StrategyDetail:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        versions = await self.version_repo.list_by_strategy(strategy_id)
        return StrategyDetail(id=strategy.id, name=strategy.name, code=strategy.code, strategy_type=strategy.strategy_type, status=strategy.status, description=strategy.description, tags=strategy.tags, latest_version_id=strategy.latest_version_id, created_at=strategy.created_at, updated_at=strategy.updated_at, versions=[StrategyVersionSummary(id=item.id, version=item.version, status=item.status, params_hash=item.params_hash, created_at=item.created_at) for item in versions])
