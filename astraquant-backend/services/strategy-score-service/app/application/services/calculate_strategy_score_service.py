from app.domain.services.admission_rule_engine import AdmissionRuleEngine
from app.domain.services.score_explanation_builder import ScoreExplanationBuilder
from app.infrastructure.clients.ai_analysis_service_client import AIAnalysisServiceClient
from app.infrastructure.clients.backtest_service_client import BacktestServiceClient
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.nats.topics import STRATEGY_SCORE_CALCULATED
from app.infrastructure.postgres.models import StrategyScoreModel
from app.infrastructure.repositories.strategy_score_repository import StrategyScoreRepository
from app.schemas.score import CalculateScoreRequest, CalculateScoreResponse
from app.scoring.ai_score import AIScore
from app.scoring.cost_score import CostScore
from app.scoring.drawdown_score import DrawdownScore
from app.scoring.out_of_sample_score import OutOfSampleScore
from app.scoring.profit_score import ProfitScore
from app.scoring.risk_score import RiskScore
from app.scoring.stability_score import StabilityScore
from app.scoring.total_score import TotalScore

class CalculateStrategyScoreService:
    def __init__(self, session): self.repo = StrategyScoreRepository(session); self.publisher = EventPublisher()
    async def execute(self, payload: CalculateScoreRequest, operator_id: str | None):
        metrics = await BacktestServiceClient().summary(payload.backtest_task_id)
        ai_result = await AIAnalysisServiceClient().result(payload.ai_task_id)
        warnings = []
        out_score, out_warnings = OutOfSampleScore().calculate(metrics); warnings += out_warnings
        ai_score, ai_warnings = AIScore().calculate(ai_result); warnings += ai_warnings
        scores = {"profit_score": ProfitScore().calculate(metrics), "drawdown_score": DrawdownScore().calculate(metrics), "stability_score": StabilityScore().calculate(metrics), "out_of_sample_score": out_score, "cost_score": CostScore().calculate(metrics), "risk_score": RiskScore().calculate(metrics), "ai_score": ai_score}
        total = TotalScore().calculate(scores)
        grade = TotalScore().grade(total)
        decision, reject_reasons, warnings = AdmissionRuleEngine().decide(metrics, scores, total, ai_result, warnings)
        suggestions = [{"type": "RUN_OUT_OF_SAMPLE_BACKTEST", "content": "建议增加样本外回测"}] if warnings else []
        detail = ScoreExplanationBuilder().build(scores, warnings, suggestions)
        model = await self.repo.create(StrategyScoreModel(strategy_id=metrics["strategy_id"], strategy_version_id=payload.strategy_version_id, backtest_task_id=payload.backtest_task_id, ai_task_id=payload.ai_task_id, total_score=total, grade=grade, decision=decision, reject_reasons=reject_reasons, warnings=warnings, suggestions=suggestions, detail_json=detail, created_by=operator_id, **scores))
        await self.publisher.publish(STRATEGY_SCORE_CALCULATED, {"event_type": STRATEGY_SCORE_CALCULATED, "score_id": model.id, "strategy_id": model.strategy_id, "strategy_version_id": model.strategy_version_id, "backtest_task_id": model.backtest_task_id, "total_score": float(model.total_score), "grade": model.grade, "decision": model.decision})
        return CalculateScoreResponse(score_id=model.id, total_score=float(model.total_score), grade=model.grade, decision=model.decision)
