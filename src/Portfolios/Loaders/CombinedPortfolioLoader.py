from tabulate import tabulate
from typing import List

from src.Portfolios.Loaders.PortfolioLoader import PortfolioLoader
from src.Brokerages.IBBrokerage import IBBrokerage
from src.Portfolios.Loaders.IBPortfolioLoader import IBPortfolioLoader
from src.Portfolios.Loaders.JSONPortfolioLoader import JSONPortfolioLoader


class CombinedPortfolioLoader(PortfolioLoader):
    def __init__(self, loaders: List[PortfolioLoader]):
        self._loaders = loaders

    @staticmethod
    def create_comb_portf_loader(external_portfolio, ib_gateway_port, ib_gateway_readonly):
        loaders = []
        if external_portfolio:
            loaders.append(JSONPortfolioLoader(external_portfolio))
        if ib_gateway_port != -1:
            IBBrokerage.connect(ib_gateway_port, ib_gateway_readonly)
            client = IBBrokerage.get_client()
            loaders.append(IBPortfolioLoader(client))
        portf_loader = CombinedPortfolioLoader(loaders)
        return portf_loader

    def _get_positions_map(self):
        # no caching, we require always fresh data
        # if performance becomes bottleneck consider creating the map only once
        positions = {}
        for loader in self._loaders:
            for name, pos in loader.positions():
                if name in positions:
                    positions[name] = {"name": name, "size": positions[name]["size"] + pos["size"]}
                else:
                    positions[name] = {"name": name, "size": pos["size"]}
        return positions

    def positions(self):
        positions = self._get_positions_map()
        # todo too wordy can be easily shortened
        for name, pos in positions.items():
            yield name, pos

    def get_position(self, name):
        positions = self._get_positions_map()
        if name in positions:
            return positions[name]

    def get_position_size(self, name):
        return super().get_position_size(name)

    def __str__(self):
        positions = self._get_positions_map()
        return tabulate(list(positions.values()), headers="keys")


if __name__ == "__main__":
    l = CombinedPortfolioLoader([
        IBPortfolioLoader(IBBrokerage.get_client()),
        JSONPortfolioLoader("../../assets/portfolio.json")
    ])
    print(l)
    print(l.get_position_size('IBKR'))
