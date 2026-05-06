import asyncio
from app.infrastructure.postgres.session import SessionLocal
from app.application.services.run_ai_analysis_service import RunAIAnalysisService
from app.workers.celery_app import celery_app

@celery_app.task(name="ai.backtest_analysis")
def run_backtest_analysis_task(ai_task_id: str):
    async def runner():
        async with SessionLocal() as session:
            await RunAIAnalysisService(session).run(ai_task_id)
            await session.commit()
    asyncio.run(runner())
