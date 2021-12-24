from abc import ABC, abstractmethod


class Executor(ABC):
    @abstractmethod
    def simple_order(self, symbol, count, limit, exchange="SMART", currency="USD"):
        """
        Executes a simple order.
        :param symbol: Symbol as recognized by the specific executor.
        :param count: Amount of shares to be bought / sold. Executors might require a specific rounding for certain assets. # todo implement this in specific executor
        :param limit: Highest willing to buy for / Lowest price willing to sell for.
        :param exchange: Exchange where the order will be placed. # todo specific for ib, shall be extraced to separate "options" parameter specific for executor
        :param currency: Currency in which the security is listed. # todo extract like the above
        """
        if count == 0:
            raise ValueError('Orders of 0 size are not supported')
        direction = 'BUY' if count > 0 else 'SELL'
        print(f'{direction} {count} of {symbol} @ {limit} (exchange={exchange}, currency={currency})')
