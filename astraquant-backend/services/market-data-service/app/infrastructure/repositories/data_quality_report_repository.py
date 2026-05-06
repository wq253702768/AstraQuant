from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import DataQualityReportModel

class DataQualityReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: dict) -> DataQualityReportModel:
        model = DataQualityReportModel(**payload)
        self.session.add(model)
        await self.session.flush()
        return model

    async def latest(self, exchange: str, symbol: str, data_type: str, timeframe: str | None) -> DataQualityReportModel | None:
        conditions = [DataQualityReportModel.exchange == exchange, DataQualityReportModel.internal_symbol == symbol, DataQualityReportModel.data_type == data_type]
        if timeframe:
            conditions.append(DataQualityReportModel.timeframe == timeframe)
        result = await self.session.execute(select(DataQualityReportModel).where(*conditions).order_by(DataQualityReportModel.created_at.desc()).limit(1))
        return result.scalar_one_or_none()
