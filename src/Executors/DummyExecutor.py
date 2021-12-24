from src.Executors.Executor import Executor


class DummyExecutor(Executor):
    """
    A dummy executor which intead of truly executing orders just prints them to console
    """
    def simple_order(self, symbol, count, limit, exchange="SMART", currency="USD"):
        super().simple_order(symbol, count, limit, exchange, currency)
