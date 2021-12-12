import json
import math

from src.Brokerages.IBBrokerage import IBBrokerage
from src.Executors.DummyExecutor import DummyExecutor
from src.Executors.IBExecutor import IBExecutor
from src.Strategies.AutoBalancer.AutoBalancerOptions import AutoBalancerOptions
from src.Strategies.CashBurner.CashBurnerOptions import CashBurnerOptions
from src.Portfolios.Loaders.CombinedPortfolioLoader import CombinedPortfolioLoader
from src.Portfolios.Loaders.IBPortfolioLoader import IBPortfolioLoader
from src.Portfolios.Loaders.JSONPortfolioLoader import JSONPortfolioLoader
from src.utils.jo_math import round_nearest
from src.utils.security_data import get_current_price


def load_desired_values(src):
    fin = open(src)
    req_balances = json.load(fin)
    print(f'Loaded required balance {req_balances["name"]}')
    return req_balances

def execute():
    portf_loader = CombinedPortfolioLoader.create_comb_portf_loader(opt.external_portfolio, opt.ib_gateway_port, opt.ib_gateway_readonly)
    print(portf_loader)


    cash_to_burn = portf_loader.get_position_size(opt.currency)
    yahoo_suffix = ''
    if opt.currency == 'EUR':
        yahoo_suffix = '.DE'
    stock_price = round_nearest(get_current_price(opt.stock_to_buy + yahoo_suffix) * 1.03, 0.05)
    wanted_amount = math.floor((cash_to_burn - 50) / stock_price)

    executor = DummyExecutor()
    if not opt.dry_run:
        if opt.ib_gateway_readonly:
            raise ValueError("Cannot send live orders to readonly connection!")
        executor = IBExecutor(IBBrokerage.get_client())
    executor.simple_order(opt.stock_to_buy, wanted_amount, stock_price, currency=opt.currency)


if __name__ == "__main__":
    AutoBalancerOptions().parse()
    opt = AutoBalancerOptions.get_args()
    AutoBalancerOptions.print_options(opt)
    desired_portfolio = load_desired_values(opt.required_balances)

    current_portfolio_value = 0
    for name, exchangeLocation, requiredPercentage in desired_portfolio.items():
        pass

    # execute()
