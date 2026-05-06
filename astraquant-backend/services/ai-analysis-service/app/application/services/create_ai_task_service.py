from datetime import UTC, datetime
from app.domain.enums.ai_task_status import AITaskStatus
from app.infrastructure.nats import topics
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.postgres.models import AITaskModel
from app.infrastructure.repositories.ai_task_repository import AITaskRepository
from app.schemas.ai_task import CreateAIBacktestAnalysisRequest, CreateAIBacktestAnalysisResponse

class CreateAITaskService:
    def __init__(self, session): self.repo = AITaskRepository(session); self.publisher = EventPublisher()
    async def execute(self, payload: CreateAIBacktestAnalysisRequest, operator_id: str | None, trace_id: str | None):
        task = await self.repo.create(AITaskModel(task_type="backtest_review", related_task_id=payload.backtest_task_id, status=AITaskStatus.QUEUED.value, progress=0, created_by=operator_id))
        await self.publisher.publish(topics.AI_ANALYSIS_REQUEST, {"event_type": topics.AI_ANALYSIS_REQUEST, "ai_task_id": task.id, "backtest_task_id": payload.backtest_task_id, "analysis_type": payload.analysis_type, "created_at": datetime.now(UTC).isoformat()})
        return CreateAIBacktestAnalysisResponse(ai_task_id=task.id, status=task.status)
