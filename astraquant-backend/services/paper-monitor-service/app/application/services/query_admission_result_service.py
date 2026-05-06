from astra_common.errors import AppError
from app.infrastructure.repositories.admission_result_repository import AdmissionResultRepository
class QueryAdmissionResultService:
    def __init__(self, session): self.repo=AdmissionResultRepository(session)
    async def execute(self, result_id: str):
        result=await self.repo.get(result_id)
        if not result: raise AppError("ADMISSION_RESULT_NOT_FOUND","准入结果不存在",404)
        return {"admission_result_id":result.id,"observation_id":result.observation_id,"decision":result.decision,"passed":result.passed,"score":str(result.score),"approval_required":result.approval_required,"approval_status":result.approval_status}
