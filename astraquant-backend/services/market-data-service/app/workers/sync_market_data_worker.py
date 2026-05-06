import asyncio
from app.infrastructure.postgres.session import SessionLocal
from app.application.services.run_sync_task_service import RunSyncTaskService
from app.workers.celery_app import celery_app

@celery_app.task(name="sync_market_data_task")
def sync_market_data_task(sync_task_id: str):
    async def runner():
        async with SessionLocal() as session:
            await RunSyncTaskService(session).mark_running(sync_task_id)
            await session.commit()
    asyncio.run(runner())
