from src.Options.BaseOptions import BaseOptions


class AutoBalancerOptions(BaseOptions):

    @staticmethod
    def parse():
        parser = super(AutoBalancerOptions, AutoBalancerOptions).parse()
        parser.add_argument('--required-balances', type=str, required=True, help="Location of json file with required balances specified")
        return parser
