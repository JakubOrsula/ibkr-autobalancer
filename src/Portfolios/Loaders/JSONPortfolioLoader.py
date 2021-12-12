import json
from tabulate import tabulate

from src.Portfolios.Loaders.PortfolioLoader import PortfolioLoader


class JSONPortfolioLoader(PortfolioLoader):
    def __init__(self, source_file):
        fin = open(source_file)
        portfolio = json.load(fin)
        print(f'Loaded portfolio {portfolio["name"]}')
        self._positions = {}
        for pos in portfolio['positions']:
            self._positions[pos['name']] = pos

    def positions(self):
        for name, pos in self._positions.items():
            yield name, pos

    def get_position(self, name):
        if name in self._positions:
            return self._positions[name]
        return {"name": name, "size": 0}

    def get_position_size(self, name):
        return super().get_position_size(name)

    def __str__(self):
        if not self._positions:
            return 'No positions'

        return tabulate(list(self._positions.values()), headers="keys", tablefmt="simple")


if __name__ == "__main__":
    loader = JSONPortfolioLoader("../../assets/portfolio.json")
    print(loader)
    print(loader.get_position_size('TSLA'))


