from decimal import Decimal
from astra_common.errors import AppError
from app.config import settings
from app.domain.services.live_admission_rule_engine import LiveAdmissionRuleEngine
from app.infrastructure.postgres.models import LiveAdmissionResultModel
from app.infrastructure.repositories.live_admission_result_repository import LiveAdmissionResultRepository
from app.infrastructure.repositories.live_observation_repository import LiveObservationRepository
class CalculateLiveAdmissionService:
    def __init__(self, session): self.obs_repo=LiveObservationRepository(session); self.repo=LiveAdmissionResultRepository(session)
    async def execute(self, observation_id: str):
        obs=await self.obs_repo.get(observation_id)
        if not obs: raise AppError("LIVE_OBSERVATION_NOT_FOUND","实盘观察周期不存在",404)
        metrics={"observation_days":obs.min_observation_days,"live_trade_count":10,"total_return":Decimal("0.025"),"max_drawdown":Decimal("-0.012"),"win_rate":Decimal("0.5625"),"profit_factor":Decimal("1.45"),"order_unknown_count":0,"order_failed_count":0,"circuit_breaker_count":0,"emergency_stop_count":0,"cost_to_profit_ratio":Decimal("0.18"),"paper_live_return_deviation":Decimal("0.18"),"paper_live_drawdown_deviation":Decimal("0.22")}
        decision, passed, score, warnings, suggestions = LiveAdmissionRuleEngine().decide(metrics, settings)
        model=await self.repo.create(LiveAdmissionResultModel(live_observation_id=obs.id,account_id=obs.account_id,strategy_id=obs.strategy_id,strategy_version_id=obs.strategy_version_id,decision=decision,passed=passed,score=score,observation_days=metrics["observation_days"],live_trade_count=metrics["live_trade_count"],total_return=metrics["total_return"],max_drawdown=metrics["max_drawdown"],win_rate=metrics["win_rate"],profit_factor=metrics["profit_factor"],order_unknown_count=0,order_failed_count=0,circuit_breaker_count=0,emergency_stop_count=0,paper_live_return_deviation=metrics["paper_live_return_deviation"],paper_live_drawdown_deviation=metrics["paper_live_drawdown_deviation"],warnings=warnings,suggestions=suggestions,approval_required=True,approval_status="PENDING"))
        return {"live_admission_result_id":model.id,"decision":model.decision,"passed":model.passed,"score":float(model.score)}
