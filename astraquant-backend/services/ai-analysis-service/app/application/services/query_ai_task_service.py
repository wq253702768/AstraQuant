from astra_common.errors import AppError
from app.infrastructure.repositories.ai_task_repository import AITaskRepository
from app.schemas.ai_task import AITaskStatusResponse

class QueryAITaskService:
    def __init__(self, session): self.repo = AITaskRepository(session)
    async def status(self, ai_task_id: str):
        task = await self.repo.get(ai_task_id)
        if not task: raise AppError("AI_TASK_NOT_FOUND", "AI任务不存在", 404)
        return AITaskStatusResponse(ai_task_id=task.id, status=task.status, current_agent=task.current_agent, progress=float(task.progress), error_message=task.error_message)
