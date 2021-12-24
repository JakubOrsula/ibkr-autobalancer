import json
import math

from src.Brokerages.IBBrokerage import IBBrokerage
from src.Executors.DummyExecutor import DummyExecutor
from src.Executors.IBExecutor import IBExecutor
from src.Strategies.AutoBalancer.AutoBalancerOptions import AutoBalancerOptions, TriggerStrategy, MitigationStrategy
from src.Portfolios.Loaders.CombinedPortfolioLoader import CombinedPortfolioLoader
from src.utils.jo_math import round_nearest
from src.utils.security_data import get_current_price
from tabulate import tabulate
from statistics import mean

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

    portf_loader = CombinedPortfolioLoader.create_comb_portf_loader(opt.external_portfolio, opt.ib_gateway_port,
                                                                    opt.ib_gateway_readonly)

    for position in desired_portfolio["balances"]:
        name = position["name"]
        ibName = position["ibName"]  # todo name should be the same as ibName hmm unify?
        currency = position["currency"]
        yahooName = position["yahooName"]
        desiredPercentage = position["desiredPercentage"]
        print(name, ibName, currency, yahooName, desiredPercentage)

    current_portfolio_value = portf_loader.get_position_size(desired_portfolio["cash"]["currency"])
    for position in desired_portfolio["balances"]:
        yahooName = position["yahooName"]
        name = position["name"]
        position_size = portf_loader.get_position_size(name)
        if position_size is None:
            position_size = 0
        position["currPrice"] = get_current_price(yahooName)
        position["positionSize"] = position_size
        current_portfolio_value += position["currPrice"] * position["positionSize"]

    print(f'Current portfolio value {current_portfolio_value}')

    for position in desired_portfolio["balances"]:
        position["value"] = position["currPrice"] * position["positionSize"]  # added to dictionary just for the looks in tabulate, can be omitted
        position["valuePercentage"] = position["value"] / current_portfolio_value * 100
        position["desiredValue"] = (position["desiredPercentage"] / 100) * current_portfolio_value
        position["deviation"] = position["desiredValue"] - position["value"]
        position["deviationPercentage"] = abs(position["valuePercentage"] - position["desiredPercentage"])

    print("Portfolio")
    print(tabulate(list(desired_portfolio["balances"]), headers="keys"))

    deviations = [position["deviationPercentage"] for position in desired_portfolio["balances"]]
    highest_deviation = max(deviations)
    lowest_deviation = min(deviations)
    average_deviation = mean(deviations)

    print(f'average deviation: {average_deviation}', f'lowest deviation: {lowest_deviation}', f'highest_deviation: {highest_deviation}', sep='\n')

    if opt.trigger_strategy == TriggerStrategy.average and average_deviation > opt.trigger_deviation:
        print(f'Tiggered by {opt.trigger_strategy.value} being {highest_deviation} which is over specified {opt.trigger_deviation}')
    elif opt.trigger_strategy == TriggerStrategy.one_min and highest_deviation > opt.trigger_deviation:
        print(f'Tiggered by {opt.trigger_strategy.value} being {highest_deviation} which is over specified {opt.trigger_deviation}') # todo abstract duplicity
    elif opt.trigger_strategy == TriggerStrategy.all_min and lowest_deviation > opt.trigger_deviation:
        print(f'Tiggered by {opt.trigger_strategy.value} being {lowest_deviation} which is over specified {opt.trigger_deviation}')  # todo abstract duplicity
    else:
        print(f'Trigger {opt.trigger_strategy.value} not fired. Not rebalancing.')

    if opt.mitigation_strategy == MitigationStrategy.sell:
        # todo add ability to specify different stock to sell than those in portfolio
        # to sell, constraints (such as those required to comply with tax test)
        # this should be done from separate json file
        # todo create Seller strategy which will sell stocks
        pass

    cash_to_burn = portf_loader.get_position_size(desired_portfolio["cash"]["currency"])
    # todo call cash burner here (it needs some tuning and strategies to burn cash)




    # execute()
