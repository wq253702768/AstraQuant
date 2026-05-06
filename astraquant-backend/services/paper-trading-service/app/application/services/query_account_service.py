from astra_common.errors import AppError
from app.infrastructure.repositories.paper_account_repository import PaperAccountRepository
class QueryAccountService:
    def __init__(self, session): self.repo=PaperAccountRepository(session)
    async def get(self, account_id: str):
        account=await self.repo.get(account_id)
        if not account: raise AppError("PAPER_ACCOUNT_NOT_FOUND","模拟账户不存在",404)
        return {"account_id":account.id,"name":account.name,"exchange":account.exchange,"currency":account.currency,"initial_balance":str(account.initial_balance),"available_balance":str(account.available_balance),"margin_used":str(account.margin_used),"unrealized_pnl":str(account.unrealized_pnl),"realized_pnl":str(account.realized_pnl),"equity":str(account.equity),"status":account.status}
