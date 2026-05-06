import asyncio
from app.application.services.build_report_service import BuildReportService
from app.infrastructure.postgres.session import SessionLocal
from app.workers.celery_app import celery_app
@celery_app.task(name="report.build")
def build_report_task(report_task_id: str):
    async def runner():
        async with SessionLocal() as session:
            await BuildReportService(session).build(report_task_id); await session.commit()
    asyncio.run(runner())
