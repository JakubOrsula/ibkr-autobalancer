from src.Executors.Executor import Executor
import ib_insync as ib_lib


class IBExecutor(Executor):
    def __init__(self, ib):
        self._ib = ib

    def simple_order(self, symbol, count, limit, exchange="SMART", currency="USD"):
        super(IBExecutor, self).simple_order(symbol, count, limit, exchange, currency)
        direction = 'BUY' if count > 0 else 'SELL'
        ib_contract = ib_lib.Stock(symbol, exchange, currency)
        # todo error checks, checks for available buy power etc
        order = ib_lib.LimitOrder(direction, count, limit)
        trade = self._ib.placeOrder(ib_contract, order)

        # todo implement some sort of polling to wait until trade is executed
        #  (and cancel and throw if it isn't within some duration)
        self._ib.sleep(5)
        return trade.log
