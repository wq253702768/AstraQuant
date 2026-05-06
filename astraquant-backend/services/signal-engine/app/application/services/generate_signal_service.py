from decimal import Decimal
from app.config import settings
from app.domain.enums.signal_status import SignalStatus
from app.domain.services.signal_dedup_service import SignalDedupService
from app.domain.services.signal_cooldown_service import SignalCooldownService
from app.domain.services.signal_payload_builder import SignalPayloadBuilder
from app.domain.services.signal_precheck_service import SignalPrecheckService
from app.infrastructure.nats.publisher import EventPublisher
from app.infrastructure.nats.topics import SIGNAL_GENERATED
from app.infrastructure.postgres.models import SignalEventModel
from app.infrastructure.repositories.signal_event_repository import SignalEventRepository
from app.runtime.strategy_registry import StrategyRegistry
from app.schemas.signal import GenerateSignalRequest, SignalResponse

_dedup=SignalDedupService(); _cooldown=SignalCooldownService()
class GenerateSignalService:
    def __init__(self, session): self.repo=SignalEventRepository(session); self.publisher=EventPublisher()
    async def execute(self, payload: GenerateSignalRequest):
        pre=SignalPrecheckService().check(payload.snapshot, payload.params, True)
        if not pre.allowed: return SignalResponse(status=SignalStatus.PRECHECK_REJECTED.value, reason=pre.reason)
        candidates=StrategyRegistry().get(payload.strategy_type).generate(payload.snapshot, payload.params)
        if not candidates: return SignalResponse(status="NO_SIGNAL", reason="未触发信号")
        sig=candidates[0]; bar_id=sig.get("bar_id") or "none"; dedup_key=_dedup.dedup_key(payload.strategy_id,payload.strategy_version_id,payload.internal_symbol,sig["signal_type"],bar_id,sig.get("position_side"))
        if not _dedup.allow(dedup_key) or not _dedup.allow_bar(payload.strategy_id,payload.internal_symbol,bar_id,sig["signal_type"]): return SignalResponse(status=SignalStatus.DEDUP_REJECTED.value, reason="重复信号")
        if not _cooldown.allow(f"{payload.strategy_id}:{payload.internal_symbol}:{sig['signal_type']}", settings.signal_cooldown_seconds): return SignalResponse(status=SignalStatus.DEDUP_REJECTED.value, reason="信号冷却中")
        market_snapshot=SignalPayloadBuilder().market_snapshot(payload.snapshot)
        model=await self.repo.create(SignalEventModel(strategy_id=payload.strategy_id,strategy_version_id=payload.strategy_version_id,exchange=payload.exchange,internal_symbol=payload.internal_symbol,signal_type=sig["signal_type"],side=sig.get("side"),position_side=sig.get("position_side"),action=sig.get("action","OPEN"),confidence=0.82,reference_price=Decimal(str(sig["reference_price"])),suggested_position_pct=Decimal(str(sig.get("suggested_position_pct",0))),leverage=Decimal(str(sig.get("leverage",1))),reason=sig["reason"],indicator_snapshot=sig.get("indicator_snapshot"),market_snapshot=market_snapshot,freshness_snapshot=pre.freshness_snapshot,risk_hint_json={},status=SignalStatus.PUBLISHED.value,dedup_key=dedup_key,bar_id=bar_id))
        await self.publisher.publish(SIGNAL_GENERATED,{"event_type":SIGNAL_GENERATED,"signal_id":model.id,"strategy_id":model.strategy_id,"strategy_version_id":model.strategy_version_id,"exchange":model.exchange,"internal_symbol":model.internal_symbol,"signal_type":model.signal_type,"action":model.action})
        return SignalResponse(signal_id=model.id,status=model.status,reason=model.reason)
