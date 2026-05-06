from app.domain.entities.instrument import Instrument

class InstrumentNormalizer:
    def normalize(self, payload: dict) -> Instrument:
        return Instrument(
            exchange=str(payload["exchange"]).upper(),
            internal_symbol=payload["internal_symbol"],
            exchange_symbol=payload["exchange_symbol"],
            base_asset=payload.get("base_asset"),
            quote_asset=payload.get("quote_asset"),
            margin_asset=payload.get("margin_asset"),
            contract_type=payload.get("contract_type", "swap"),
            tick_size=payload.get("tick_size"),
            lot_size=payload.get("lot_size"),
            min_size=payload.get("min_size"),
            contract_value=payload.get("contract_value"),
            price_precision=payload.get("price_precision"),
            size_precision=payload.get("size_precision"),
            status=payload.get("status", "active"),
            raw_json=payload,
        )
