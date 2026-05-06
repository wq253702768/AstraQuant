from app.domain.enums.account_status import AccountStatus
from app.infrastructure.postgres.models import PaperAccountModel
from app.infrastructure.repositories.paper_account_repository import PaperAccountRepository
from app.schemas.account import CreatePaperAccountRequest, PaperAccountResponse
class CreatePaperAccountService:
    def __init__(self, session): self.repo=PaperAccountRepository(session)
    async def execute(self, payload: CreatePaperAccountRequest, created_by: str|None):
        model=await self.repo.create(PaperAccountModel(name=payload.name, exchange=payload.exchange, currency=payload.currency, initial_balance=payload.initial_balance, available_balance=payload.initial_balance, equity=payload.initial_balance, status=AccountStatus.ACTIVE.value, created_by=created_by))
        return PaperAccountResponse(account_id=model.id,name=model.name,initial_balance=str(model.initial_balance),equity=str(model.equity),status=model.status)
