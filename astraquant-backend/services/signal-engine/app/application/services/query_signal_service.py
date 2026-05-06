from astra_common.errors import AppError
from app.infrastructure.repositories.signal_event_repository import SignalEventRepository
class QuerySignalService:
    def __init__(self, session): self.repo=SignalEventRepository(session)
    async def list(self,page:int=1,page_size:int=20):
        rows,total=await self.repo.list(page,page_size); return {"items":[self._row(r) for r in rows],"total":total}
    async def get(self, signal_id: str):
        row=await self.repo.get(signal_id)
        if not row: raise AppError("SIGNAL_NOT_FOUND","信号不存在",404)
        return self._row(row)
    def _row(self,r): return {"id":r.id,"strategy_id":r.strategy_id,"strategy_version_id":r.strategy_version_id,"exchange":r.exchange,"internal_symbol":r.internal_symbol,"signal_type":r.signal_type,"action":r.action,"reference_price":str(r.reference_price),"leverage":str(r.leverage),"confidence":float(r.confidence or 0),"status":r.status,"reason":r.reason,"indicator_snapshot":r.indicator_snapshot,"market_snapshot":r.market_snapshot,"freshness_snapshot":r.freshness_snapshot,"risk_hint_json":r.risk_hint_json,"created_at":r.created_at}
