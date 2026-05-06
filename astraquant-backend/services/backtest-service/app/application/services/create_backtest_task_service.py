from app.domain.enums.backtest_status import BacktestStatus
from app.domain.services.backtest_validation_service import BacktestValidationService
from app.infrastructure.postgres.models import BacktestTaskModel
from app.infrastructure.repositories.backtest_task_repository import BacktestTaskRepository
from app.schemas.backtest import CreateBacktestRequest, CreateBacktestResponse

class CreateBacktestTaskService:
    def __init__(self, session):
        self.repo = BacktestTaskRepository(session)
        self.validator = BacktestValidationService()

    async def execute(self, payload: CreateBacktestRequest, operator_id: str | None) -> CreateBacktestResponse:
        self.validator.validate_request(payload.exchange, payload.symbols, payload.timeframe, payload.start_time, payload.end_time, payload.initial_capital)
        task = await self.repo.create(BacktestTaskModel(strategy_id="00000000-0000-0000-0000-000000000001", strategy_version_id=payload.strategy_version_id, exchange=payload.exchange, symbols=payload.symbols, timeframe=payload.timeframe, start_time=payload.start_time, end_time=payload.end_time, initial_capital=payload.initial_capital, cost_model=payload.cost_model, risk_model=payload.risk_model, status=BacktestStatus.QUEUED.value, progress=0, current_stage="queued", created_by=operator_id))
        return CreateBacktestResponse(task_id=task.id, status=task.status)
