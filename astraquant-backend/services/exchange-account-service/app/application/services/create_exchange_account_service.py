from app.infrastructure.postgres.models import ExchangeAccountModel
from app.infrastructure.repositories.exchange_account_repository import ExchangeAccountRepository
from app.schemas.exchange_account import CreateExchangeAccountRequest, ExchangeAccountResponse
class CreateExchangeAccountService:
    def __init__(self, session): self.repo=ExchangeAccountRepository(session)
    async def execute(self, payload: CreateExchangeAccountRequest, operator_id: str|None):
        model=await self.repo.create(ExchangeAccountModel(name=payload.name,exchange=payload.exchange,account_type=payload.account_type,environment=payload.environment,status="CREATED",trading_enabled=False,read_enabled=True,default_currency=payload.default_currency,expected_outbound_ip=payload.expected_outbound_ip,created_by=operator_id))
        return ExchangeAccountResponse(account_id=model.id,status=model.status)
