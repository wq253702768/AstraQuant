from app.workers.celery_app import celery_app

@celery_app.task(name="backtest.run")
def run_backtest_task(task_id: str):
    return {"task_id": task_id, "status": "accepted"}
