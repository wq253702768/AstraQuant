from decimal import Decimal
from itertools import count
from app.domain.entities.backtest_order import BacktestOrder
from app.engine.signal_generator import TradeSignal

_counter = count(1)

class OrderSimulator:
    def create_order(self, signal: TradeSignal, initial_capital: Decimal) -> BacktestOrder:
        size = signal.size or Decimal("0")
        if size <= 1:
            notional = initial_capital * size * signal.leverage
            quantity = notional / signal.price
        else:
            quantity = size
        return BacktestOrder(order_time=signal.signal_time, symbol=signal.symbol, side=signal.side, position_side=signal.position_side, action=signal.action, order_type="IOC", price=signal.price, size=quantity, leverage=signal.leverage, cl_ord_id=f"BT_{next(_counter):06d}", reason=signal.reason)
