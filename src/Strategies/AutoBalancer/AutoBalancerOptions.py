from src.Options.BaseOptions import BaseOptions
import argparse
import enum


class EnumAction(argparse.Action):
    """
    Argparse action for handling Enums
    """
    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)

        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        value = self._enum(values)
        setattr(namespace, self.dest, value)


class TriggerStrategy(enum.Enum):
    one_min = "one-min"
    all_min = "all-min"
    average = "average"


class MitigationStrategy(enum.Enum):
    cash_only = "cash-only"  # no selling will take place and the difference will be settled just by cash
    sell = "sell"  # stock will be sold to accumulate enough to rebalance portfolio
    margin = "margin" # todo buy using margin - this needs more specs

class AutoBalancerOptions(BaseOptions):

    @staticmethod
    def parse():
        parser = super(AutoBalancerOptions, AutoBalancerOptions).parse()
        parser.add_argument('--required-balances', type=str, required=True, help="Location of json file with required balances specified")
        parser.add_argument('--trigger-strategy', type=TriggerStrategy, action=EnumAction, required=True, help="What will trigger rebalance. See docs for possible values and meaning")
        parser.add_argument('--mitigation-strategy', type=MitigationStrategy, action=EnumAction, required=True, help="How the portfolio will be rebalanced. See docs for possible values and meaning")
        return parser
