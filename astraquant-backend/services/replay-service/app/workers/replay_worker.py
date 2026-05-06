from app.workers.celery_app import celery_app

@celery_app.task(name="replay.build")
def build_replay_task(backtest_task_id: str, force_rebuild: bool = False):
    return {"backtest_task_id": backtest_task_id, "force_rebuild": force_rebuild, "status": "accepted"}
