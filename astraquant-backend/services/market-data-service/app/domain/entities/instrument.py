from dataclasses import dataclass

@dataclass(frozen=True)
class Instrument:
    exchange: str
    internal_symbol: str
    exchange_symbol: str
    base_asset: str | None
    quote_asset: str | None
    margin_asset: str | None
    contract_type: str
    tick_size: str | None
    lot_size: str | None
    min_size: str | None
    contract_value: str | None
    price_precision: int | None
    size_precision: int | None
    status: str
    raw_json: dict | None = None
