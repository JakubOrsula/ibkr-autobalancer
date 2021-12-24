from abc import ABC, abstractmethod


class PortfolioLoader(ABC):
    """
    Loads portfolio positions from a specific source. Provides convenience methods to query position sizes.
    """

    @abstractmethod
    def positions(self):
        """
        Generator to yield all positions in portfolio
        :return: (security_name, security_object), where security_object contains details about the position such as count or average price
        """
        pass

    @abstractmethod
    def get_position(self, name):
        """
        Return security details for a security name specified by param name
        :param name: which security details you want
        :return: security details, None if not found
        """
        pass

    @abstractmethod
    def get_position_size(self, name):
        """
        Same as get_position but provides only the price
        :param name:
        :return: price or None
        """
        pos = self.get_position(name)
        if pos:
            return pos['size']
