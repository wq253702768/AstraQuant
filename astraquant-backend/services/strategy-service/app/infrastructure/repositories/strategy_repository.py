from datetime import UTC, datetime
from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import StrategyModel, StrategyVersionModel

class StrategyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def code_exists(self, code: str, exclude_id: str | None = None) -> bool:
        conditions = [StrategyModel.code == code]
        if exclude_id:
            conditions.append(StrategyModel.id != exclude_id)
        result = await self.session.execute(select(StrategyModel.id).where(*conditions))
        return result.scalar_one_or_none() is not None

    async def create(self, model: StrategyModel) -> StrategyModel:
        self.session.add(model)
        await self.session.flush()
        return model

    async def get(self, strategy_id: str) -> StrategyModel | None:
        result = await self.session.execute(select(StrategyModel).where(StrategyModel.id == strategy_id, StrategyModel.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def update_basic(self, strategy: StrategyModel, name: str | None, description: str | None, tags, operator_id: str) -> StrategyModel:
        if name is not None:
            strategy.name = name
        if description is not None:
            strategy.description = description
        if tags is not None:
            strategy.tags = tags
        strategy.updated_by = operator_id
        strategy.updated_at = datetime.now(UTC)
        await self.session.flush()
        return strategy

    async def archive(self, strategy: StrategyModel, operator_id: str) -> StrategyModel:
        strategy.status = "ARCHIVED"
        strategy.archived_at = datetime.now(UTC)
        strategy.updated_by = operator_id
        strategy.updated_at = datetime.now(UTC)
        await self.session.flush()
        return strategy

    async def set_latest_version(self, strategy_id: str, version_id: str) -> None:
        await self.session.execute(update(StrategyModel).where(StrategyModel.id == strategy_id).values(latest_version_id=version_id, updated_at=datetime.now(UTC)))

    async def list(self, status: str | None, strategy_type: str | None, keyword: str | None, page: int, page_size: int) -> tuple[list[StrategyModel], int]:
        conditions = [StrategyModel.deleted_at.is_(None)]
        if status:
            conditions.append(StrategyModel.status == status)
        if strategy_type:
            conditions.append(StrategyModel.strategy_type == strategy_type)
        if keyword:
            pattern = f"%{keyword}%"
            conditions.append(or_(StrategyModel.name.ilike(pattern), StrategyModel.code.ilike(pattern)))
        total = (await self.session.execute(select(func.count()).select_from(StrategyModel).where(*conditions))).scalar_one()
        result = await self.session.execute(select(StrategyModel).where(*conditions).order_by(StrategyModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size))
        return list(result.scalars()), int(total)

    async def latest_version(self, strategy_id: str) -> StrategyVersionModel | None:
        result = await self.session.execute(select(StrategyVersionModel).where(StrategyVersionModel.strategy_id == strategy_id).order_by(StrategyVersionModel.created_at.desc()).limit(1))
        return result.scalar_one_or_none()
