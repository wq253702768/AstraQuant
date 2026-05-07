from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import StrategyTemplateModel
from uuid import UUID

class StrategyTemplateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_enabled(self) -> list[StrategyTemplateModel]:
        result = await self.session.execute(select(StrategyTemplateModel).where(StrategyTemplateModel.enabled.is_(True)).order_by(StrategyTemplateModel.sort_order, StrategyTemplateModel.code))
        return list(result.scalars())

    async def first_enabled(self) -> StrategyTemplateModel | None:
        result = await self.session.execute(select(StrategyTemplateModel).where(StrategyTemplateModel.enabled.is_(True)).order_by(StrategyTemplateModel.sort_order, StrategyTemplateModel.code).limit(1))
        return result.scalar_one_or_none()

    async def get(self, template_id_or_code: str) -> StrategyTemplateModel | None:
        try:
            UUID(str(template_id_or_code))
            condition = (StrategyTemplateModel.id == template_id_or_code) | (StrategyTemplateModel.code == template_id_or_code)
        except ValueError:
            condition = StrategyTemplateModel.code == template_id_or_code
        result = await self.session.execute(select(StrategyTemplateModel).where(condition))
        return result.scalar_one_or_none()

    async def upsert_seed(self, row: dict) -> StrategyTemplateModel:
        existing = await self.get(row["code"])
        if existing:
            for key, value in row.items():
                setattr(existing, key, value)
            return existing
        model = StrategyTemplateModel(**row)
        self.session.add(model)
        await self.session.flush()
        return model
