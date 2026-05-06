from app.config import settings
from app.infrastructure.postgres.models import AIModelCallLogModel
from app.infrastructure.repositories.ai_model_call_log_repository import AIModelCallLogRepository

class ModelCallLogService:
    def __init__(self, session): self.repo = AIModelCallLogRepository(session)
    async def log_mock_call(self, ai_task_id: str, agent_name: str, input_data_hash: str, output_json: dict):
        return await self.repo.create(AIModelCallLogModel(ai_task_id=ai_task_id, agent_name=agent_name, model_provider="OpenAI", model_name=settings.openai_model_name, model_version=settings.openai_model_version, temperature=settings.openai_temperature, max_context=128000, input_tokens=100, output_tokens=100, prompt_version=agent_name.replace("_agent", "_v1.0"), input_data_hash=input_data_hash, latency_ms=1, request_json={"mock": True}, output_json=output_json))
