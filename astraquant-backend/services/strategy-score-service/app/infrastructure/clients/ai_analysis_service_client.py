class AIAnalysisServiceClient:
    async def result(self, ai_task_id: str | None) -> dict | None:
        if not ai_task_id: return None
        return {"risk_level": "MEDIUM", "final_recommendation": "RETEST_REQUIRED"}
