from src.Executors.Executor import Executor


class DummyExecutor(Executor):
    def simple_order(self, symbol, count, limit, exchange="SMART", currency="USD"):
        super().simple_order(symbol, count, limit, exchange, currency)
