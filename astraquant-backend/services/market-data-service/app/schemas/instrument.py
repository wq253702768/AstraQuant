from pydantic import BaseModel

class InstrumentResponse(BaseModel):
    exchange: str
    internal_symbol: str
    exchange_symbol: str
    base_asset: str | None = None
    quote_asset: str | None = None
    margin_asset: str | None = None
    contract_type: str
    tick_size: str | None = None
    lot_size: str | None = None
    min_size: str | None = None
    contract_value: str | None = None
    status: str
