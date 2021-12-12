from abc import ABC, abstractmethod


class PortfolioLoader(ABC):

    @abstractmethod
    def positions(self):
        pass

    @abstractmethod
    def get_position(self, name):
        pass

    @abstractmethod
    def get_position_size(self, name):
        return self.get_position(name)['size']
