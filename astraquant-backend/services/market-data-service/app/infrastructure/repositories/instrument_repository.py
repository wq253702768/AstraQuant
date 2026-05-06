from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.instrument import Instrument
from app.infrastructure.postgres.models import InstrumentConfigModel

class InstrumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, item: Instrument) -> InstrumentConfigModel:
        result = await self.session.execute(select(InstrumentConfigModel).where(InstrumentConfigModel.exchange == item.exchange, InstrumentConfigModel.internal_symbol == item.internal_symbol))
        model = result.scalar_one_or_none()
        values = dict(exchange=item.exchange, internal_symbol=item.internal_symbol, exchange_symbol=item.exchange_symbol, base_asset=item.base_asset, quote_asset=item.quote_asset, margin_asset=item.margin_asset, contract_type=item.contract_type, tick_size=Decimal(item.tick_size) if item.tick_size else None, lot_size=Decimal(item.lot_size) if item.lot_size else None, min_size=Decimal(item.min_size) if item.min_size else None, contract_value=Decimal(item.contract_value) if item.contract_value else None, price_precision=item.price_precision, size_precision=item.size_precision, status=item.status, raw_json=item.raw_json)
        if model is None:
            model = InstrumentConfigModel(**values)
            self.session.add(model)
        else:
            for key, value in values.items():
                setattr(model, key, value)
        await self.session.flush()
        return model

    async def list(self, exchange: str | None, symbol: str | None, status: str | None) -> list[InstrumentConfigModel]:
        conditions = []
        if exchange: conditions.append(InstrumentConfigModel.exchange == exchange)
        if symbol: conditions.append(InstrumentConfigModel.internal_symbol == symbol)
        if status: conditions.append(InstrumentConfigModel.status == status)
        result = await self.session.execute(select(InstrumentConfigModel).where(*conditions).order_by(InstrumentConfigModel.internal_symbol.asc()))
        return list(result.scalars())
