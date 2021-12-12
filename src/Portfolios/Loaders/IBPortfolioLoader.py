from tabulate import tabulate

from src.Brokerages.IBBrokerage import IBBrokerage
from src.Portfolios.Loaders.PortfolioLoader import PortfolioLoader


class IBPortfolioLoader(PortfolioLoader):
    def __init__(self, ib):
        self._ib = ib

    def positions(self):
        positions = self._ib.positions()
        for pos in positions:
            yield pos.contract.symbol, {"name": pos.contract.symbol, "size": pos.position}
        accVals = self._ib.accountValues()
        for val in accVals:
            if val.tag == "TotalCashBalance":
                if val.currency == "BASE":
                    continue
                yield val.currency, {"name": val.currency, "size": float(val.value)}
        # cash_to_burn = [v for v in ib.accountValues() if v.tag == 'AvailableFunds' and v.currency == 'EUR'][0].value

    # todo there's a weird behaviour - ib returns position size rounded down to nearest integer
    def get_position(self, name):
        for i_name, pos in self.positions():
            if name == i_name:
                return pos
        return {"name": name, "size": 0}

    def get_position_size(self, name):
        return super().get_position_size(name)

    def __str__(self):
        positions = [pos for _, pos in self.positions()]
        return tabulate(positions, headers="keys")


if __name__ == "__main__":
    client = IBBrokerage.get_client()
    l = IBPortfolioLoader(client)
    print(l)
    print(l.get_position_size('IBKR'))
