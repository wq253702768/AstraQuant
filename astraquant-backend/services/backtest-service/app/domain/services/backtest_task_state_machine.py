from astra_common.errors import AppError
from app.domain.enums.backtest_status import BacktestStatus

class BacktestTaskStateMachine:
    allowed = {
        BacktestStatus.CREATED.value: {BacktestStatus.QUEUED.value, BacktestStatus.FAILED.value},
        BacktestStatus.QUEUED.value: {BacktestStatus.DATA_LOADING.value, BacktestStatus.CANCELED.value, BacktestStatus.FAILED.value},
        BacktestStatus.DATA_LOADING.value: {BacktestStatus.DATA_VALIDATING.value, BacktestStatus.FAILED.value},
        BacktestStatus.DATA_VALIDATING.value: {BacktestStatus.RUNNING.value, BacktestStatus.FAILED.value},
        BacktestStatus.RUNNING.value: {BacktestStatus.CALCULATING_METRICS.value, BacktestStatus.CANCELED.value, BacktestStatus.FAILED.value},
        BacktestStatus.CALCULATING_METRICS.value: {BacktestStatus.BUILDING_REPLAY.value, BacktestStatus.FAILED.value},
        BacktestStatus.BUILDING_REPLAY.value: {BacktestStatus.BUILDING_REPORT.value, BacktestStatus.FAILED.value},
        BacktestStatus.BUILDING_REPORT.value: {BacktestStatus.COMPLETED.value, BacktestStatus.FAILED.value},
    }
    def ensure(self, from_status: str, to_status: str) -> None:
        if to_status not in self.allowed.get(from_status, set()) and from_status != to_status:
            raise AppError("INVALID_BACKTEST_STATE_TRANSITION", f"非法回测状态流转：{from_status}->{to_status}", 409)
