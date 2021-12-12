from src.Options.BaseOptions import BaseOptions


class CashBurnerOptions(BaseOptions):

    @staticmethod
    def parse():
        parser = super(CashBurnerOptions, CashBurnerOptions).parse()
        parser.add_argument('--currency', type=str, default='EUR', help="Which currency do you want to burn")
        parser.add_argument('--stock-to-buy', type=str, required=True, help="Which stock should be bought for the currency")
        parser.add_argument('--exchange-location', type=str, required=True, help="Location of exchange where the stock will be bought (for yahoo price lookup). Examples: DE for Xetra/IBIS, AS for Amsterdam/EURONEXT")
        parser.add_argument('--exchange', type=str, default='SMART',  help="Exchange where the stock will be bought")
        return parser
