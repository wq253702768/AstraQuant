from app.domain.services.live_report_builder import LiveReportBuilder
class BuildLiveDailyReportService:
    async def execute(self): return LiveReportBuilder().build({})
