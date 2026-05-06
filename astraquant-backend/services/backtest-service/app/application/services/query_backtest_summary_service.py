from astra_common.errors import AppError
from app.infrastructure.repositories.backtest_result_repository import BacktestResultRepository
from app.schemas.backtest import BacktestSummaryResponse

class QueryBacktestSummaryService:
    def __init__(self, session):
        self.repo = BacktestResultRepository(session)
    async def execute(self, task_id: str) -> BacktestSummaryResponse:
        result = await self.repo.get_by_task(task_id)
        if not result:
            raise AppError("BACKTEST_RESULT_NOT_FOUND", "回测结果不存在", 404)
        return BacktestSummaryResponse(task_id=task_id, total_return=str(result.total_return), annual_return=str(result.annual_return), final_equity=str(result.final_equity), max_drawdown=str(result.max_drawdown), win_rate=str(result.win_rate), profit_loss_ratio=str(result.profit_loss_ratio), profit_factor=str(result.profit_factor), trade_count=result.trade_count, max_consecutive_losses=result.max_consecutive_losses, fee_total=str(result.fee_total), slippage_total=str(result.slippage_total), funding_fee_total=str(result.funding_fee_total), net_profit=str(result.net_profit), decision=result.decision)
