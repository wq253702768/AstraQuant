from astra_common.errors import AppError
from app.domain.enums.sync_status import SyncStatus
from app.domain.services.timeframe import SUPPORTED_EXCHANGES, SUPPORTED_SYMBOLS, SUPPORTED_TIMEFRAMES
from app.infrastructure.postgres.models import MarketDataSyncTaskModel
from app.infrastructure.repositories.sync_task_repository import SyncTaskRepository
from app.schemas.sync import CreateSyncTaskRequest, CreateSyncTaskResponse

class CreateSyncTaskService:
    def __init__(self, session):
        self.repo = SyncTaskRepository(session)

    async def execute(self, payload: CreateSyncTaskRequest, operator_id: str | None) -> CreateSyncTaskResponse:
        if payload.exchange not in SUPPORTED_EXCHANGES:
            raise AppError("UNSUPPORTED_EXCHANGE", "不支持的交易所", 422)
        unsupported = [item for item in payload.symbols if item not in SUPPORTED_SYMBOLS]
        if unsupported:
            raise AppError("UNSUPPORTED_SYMBOL", f"不支持的品种：{unsupported}", 422)
        if payload.timeframes:
            bad_timeframes = [item for item in payload.timeframes if item not in SUPPORTED_TIMEFRAMES]
            if bad_timeframes:
                raise AppError("UNSUPPORTED_TIMEFRAME", f"不支持的周期：{bad_timeframes}", 422)
        task = await self.repo.create(MarketDataSyncTaskModel(exchange=payload.exchange, symbols=payload.symbols, data_types=payload.data_types, timeframes=payload.timeframes, start_time=payload.start_time, end_time=payload.end_time, force_resync=payload.force_resync, status=SyncStatus.QUEUED.value, progress=0, current_stage="queued", created_by=operator_id))
        return CreateSyncTaskResponse(sync_task_id=task.id, status=task.status)
