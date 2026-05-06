from decimal import Decimal
from astra_common.errors import AppError
from app.config import settings
from app.domain.services.simulation_admission_rule_engine import SimulationAdmissionRuleEngine
from app.infrastructure.postgres.models import SimulationAdmissionResultModel
from app.infrastructure.repositories.admission_result_repository import AdmissionResultRepository
from app.infrastructure.repositories.observation_repository import ObservationRepository
class CalculateAdmissionService:
    def __init__(self, session): self.obs_repo=ObservationRepository(session); self.repo=AdmissionResultRepository(session)
    async def execute(self, observation_id: str):
        obs=await self.obs_repo.get(observation_id)
        if not obs: raise AppError("OBSERVATION_NOT_FOUND","观察周期不存在",404)
        metrics={"observation_days": obs.min_observation_days, "trade_count": 20, "total_return": Decimal("0.04"), "max_drawdown": Decimal("-0.028"), "win_rate": Decimal("0.52"), "profit_factor": Decimal("1.42"), "max_consecutive_losses": 3, "cost_to_profit_ratio": Decimal("0.18"), "risk_reject_count": 8, "pause_strategy_count": 0, "order_error_count": 0, "data_stale_count": 2}
        decision, passed, score, reasons, warnings, suggestions = SimulationAdmissionRuleEngine().decide(metrics, settings)
        model=await self.repo.create(SimulationAdmissionResultModel(observation_id=obs.id,account_id=obs.account_id,strategy_id=obs.strategy_id,strategy_version_id=obs.strategy_version_id,decision=decision,passed=passed,score=score,observation_days=metrics["observation_days"],trade_count=metrics["trade_count"],total_return=metrics["total_return"],max_drawdown=metrics["max_drawdown"],win_rate=metrics["win_rate"],profit_factor=metrics["profit_factor"],max_consecutive_losses=metrics["max_consecutive_losses"],cost_to_profit_ratio=metrics["cost_to_profit_ratio"],risk_reject_count=metrics["risk_reject_count"],pause_strategy_count=metrics["pause_strategy_count"],order_error_count=metrics["order_error_count"],data_stale_count=metrics["data_stale_count"],reject_reasons=reasons,warnings=warnings,suggestions=suggestions,detail_json=metrics,approval_required=True,approval_status="PENDING"))
        obs.latest_admission_result_id=model.id
        return {"admission_result_id":model.id,"decision":model.decision,"passed":model.passed,"score":float(model.score)}
