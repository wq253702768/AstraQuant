from app.domain.services.instrument_normalizer import InstrumentNormalizer
from app.infrastructure.clients.exchange_gateway_client import ExchangeGatewayClient
from app.infrastructure.repositories.instrument_repository import InstrumentRepository

class SyncInstrumentsService:
    def __init__(self, session, client: ExchangeGatewayClient | None = None):
        self.repo = InstrumentRepository(session)
        self.client = client or ExchangeGatewayClient()
        self.normalizer = InstrumentNormalizer()

    async def sync(self, exchange: str, symbols: list[str]) -> int:
        count = 0
        for symbol in symbols:
            items = await self.client.get_instruments(exchange, "swap", symbol)
            for payload in items:
                await self.repo.upsert(self.normalizer.normalize(payload))
                count += 1
        return count
