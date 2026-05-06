from app.domain.enums.live_observation_status import LiveObservationStatus
from app.infrastructure.postgres.models import LiveObservationModel
from app.infrastructure.repositories.live_observation_repository import LiveObservationRepository
from app.schemas.observation import CreateLiveObservationRequest, LiveObservationResponse
class CreateLiveObservationService:
    def __init__(self, session): self.repo=LiveObservationRepository(session)
    async def execute(self, payload: CreateLiveObservationRequest, operator_id: str|None):
        model=await self.repo.create(LiveObservationModel(account_id=payload.account_id,strategy_id=payload.strategy_id,strategy_version_id=payload.strategy_version_id,exchange=payload.exchange,symbols=payload.symbols,start_time=payload.start_time,observation_type=payload.observation_type,min_observation_days=payload.min_observation_days,status=LiveObservationStatus.RUNNING.value,created_by=operator_id))
        return LiveObservationResponse(live_observation_id=model.id,status=model.status)
