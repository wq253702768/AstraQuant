from app.infrastructure.repositories.ai_model_call_log_repository import AIModelCallLogRepository

class QueryModelCallService:
    def __init__(self, session): self.repo = AIModelCallLogRepository(session)
    async def list(self, ai_task_id: str):
        rows = await self.repo.list_by_task(ai_task_id)
        return {"items": [{"agent_name": r.agent_name, "model_provider": r.model_provider, "model_name": r.model_name, "model_version": r.model_version, "temperature": str(r.temperature), "max_context": r.max_context, "input_tokens": r.input_tokens, "output_tokens": r.output_tokens, "prompt_version": r.prompt_version, "input_data_hash": r.input_data_hash, "latency_ms": r.latency_ms, "created_at": r.created_at} for r in rows]}
