from app.config import settings

class OpenAIClient:
    async def complete_json(self, agent_name: str, prompt: str, input_data: dict) -> dict:
        return {"model_provider": "OpenAI", "model_name": settings.openai_model_name, "model_version": settings.openai_model_version, "temperature": settings.openai_temperature, "input_tokens": len(str(input_data)) // 4, "output_tokens": 256, "latency_ms": 1}
