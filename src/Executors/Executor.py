from abc import ABC, abstractmethod


class Executor(ABC):
    @abstractmethod
    def simple_order(self, symbol, count, limit, exchange="SMART", currency="USD"):
        if count == 0:
            raise ValueError('Orders of 0 size are not supported')
        direction = 'BUY' if count > 0 else 'SELL'
        print(f'{direction} {count} of {symbol} @ {limit} (exchange={exchange}, currency={currency})')
