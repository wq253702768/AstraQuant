from app.infrastructure.repositories.data_quality_report_repository import DataQualityReportRepository

class QueryQualityReportService:
    def __init__(self, session):
        self.repo = DataQualityReportRepository(session)
    async def latest(self, exchange: str, symbol: str, data_type: str, timeframe: str | None):
        return await self.repo.latest(exchange, symbol, data_type, timeframe)
