from astra_common.errors import AppError
from app.infrastructure.repositories.ai_agent_output_repository import AIAgentOutputRepository
from app.infrastructure.repositories.ai_task_repository import AITaskRepository

class QueryAIResultService:
    def __init__(self, session): self.task_repo = AITaskRepository(session); self.output_repo = AIAgentOutputRepository(session)
    async def result(self, ai_task_id: str):
        task = await self.task_repo.get(ai_task_id)
        if not task: raise AppError("AI_TASK_NOT_FOUND", "AI任务不存在", 404)
        outputs = await self.output_repo.list_by_task(ai_task_id)
        return {"ai_task_id": task.id, "status": task.status, "summary": (task.result_json or {}).get("summary"), "agents": [item.output_json for item in outputs]}
