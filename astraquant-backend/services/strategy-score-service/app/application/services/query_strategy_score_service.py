from astra_common.errors import AppError
from app.infrastructure.repositories.strategy_score_repository import StrategyScoreRepository

class QueryStrategyScoreService:
    def __init__(self, session): self.repo = StrategyScoreRepository(session)
    async def get(self, score_id: str):
        score = await self.repo.get(score_id)
        if not score: raise AppError("STRATEGY_SCORE_NOT_FOUND", "策略评分不存在", 404)
        return self._to_dict(score)
    async def latest(self, strategy_version_id: str):
        score = await self.repo.latest_by_version(strategy_version_id)
        if not score: raise AppError("STRATEGY_SCORE_NOT_FOUND", "策略评分不存在", 404)
        return {"score_id": score.id, "total_score": float(score.total_score), "grade": score.grade, "decision": score.decision, "created_at": score.created_at}
    def _to_dict(self, score):
        return {"score_id": score.id, "strategy_id": score.strategy_id, "strategy_version_id": score.strategy_version_id, "backtest_task_id": score.backtest_task_id, "ai_task_id": score.ai_task_id, "total_score": float(score.total_score), "grade": score.grade, "decision": score.decision, "scores": {"profit_score": float(score.profit_score), "drawdown_score": float(score.drawdown_score), "stability_score": float(score.stability_score), "out_of_sample_score": float(score.out_of_sample_score), "cost_score": float(score.cost_score), "risk_score": float(score.risk_score), "ai_score": float(score.ai_score)}, "warnings": score.warnings or [], "suggestions": score.suggestions or []}
