from app.domain.enums.observation_status import ObservationStatus
from app.infrastructure.postgres.models import SimulationObservationModel
from app.infrastructure.repositories.observation_repository import ObservationRepository
from app.schemas.observation import CreateObservationRequest, ObservationResponse
class CreateObservationService:
    def __init__(self, session): self.repo=ObservationRepository(session)
    async def execute(self, payload: CreateObservationRequest, created_by: str|None):
        model=await self.repo.create(SimulationObservationModel(account_id=payload.account_id,strategy_id=payload.strategy_id,strategy_version_id=payload.strategy_version_id,exchange=payload.exchange,symbols=payload.symbols,start_time=payload.start_time,min_observation_days=payload.min_observation_days,status=ObservationStatus.RUNNING.value,created_by=created_by))
        return ObservationResponse(observation_id=model.id,status=model.status)
