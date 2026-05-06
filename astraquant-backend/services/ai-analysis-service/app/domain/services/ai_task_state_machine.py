from astra_common.errors import AppError
from app.domain.enums.ai_task_status import AITaskStatus

class AITaskStateMachine:
    allowed = {
        AITaskStatus.CREATED.value: {AITaskStatus.QUEUED.value, AITaskStatus.FAILED.value},
        AITaskStatus.QUEUED.value: {AITaskStatus.LOADING_DATA.value, AITaskStatus.CANCELED.value, AITaskStatus.FAILED.value},
        AITaskStatus.LOADING_DATA.value: {AITaskStatus.RUNNING.value, AITaskStatus.FAILED.value},
        AITaskStatus.RUNNING.value: {AITaskStatus.VALIDATING_OUTPUT.value, AITaskStatus.CANCELED.value, AITaskStatus.FAILED.value},
        AITaskStatus.VALIDATING_OUTPUT.value: {AITaskStatus.COMPLETED.value, AITaskStatus.FAILED.value},
    }
    def ensure(self, from_status: str, to_status: str) -> None:
        if to_status not in self.allowed.get(from_status, set()) and from_status != to_status:
            raise AppError("INVALID_AI_TASK_STATE_TRANSITION", f"非法AI任务状态流转：{from_status}->{to_status}", 409)
