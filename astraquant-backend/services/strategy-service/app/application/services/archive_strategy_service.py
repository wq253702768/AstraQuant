from astra_common.errors import AppError
from app.infrastructure.db.models import StrategyStatusLogModel
from app.infrastructure.repositories.strategy_repository import StrategyRepository
from app.infrastructure.repositories.strategy_status_log_repository import StrategyStatusLogRepository
from app.schemas.strategy import StatusChangeResponse


class ArchiveStrategyService:
    def __init__(self, session):
        self.strategy_repo = StrategyRepository(session)
        self.log_repo = StrategyStatusLogRepository(session)

    async def execute(self, strategy_id: str, reason: str, operator_id: str) -> StatusChangeResponse:
        strategy = await self.strategy_repo.get(strategy_id)
        if strategy is None:
            raise AppError("STRATEGY_NOT_FOUND", "策略不存在", 404)
        old_status = strategy.status
        await self.strategy_repo.archive(strategy, operator_id)
        await self.log_repo.create(StrategyStatusLogModel(strategy_id=strategy.id, strategy_version_id=None, from_status=old_status, to_status=strategy.status, reason=reason, operator_id=operator_id))
        return StatusChangeResponse(strategy_id=strategy.id, status=strategy.status)
