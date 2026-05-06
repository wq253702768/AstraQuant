from abc import ABC, abstractmethod
from app.engine.signal_generator import TradeSignal

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, rows: list[dict], params: dict) -> list[TradeSignal]:
        raise NotImplementedError
