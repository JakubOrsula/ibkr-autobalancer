import math
import ib_insync as ib_lib

from src.utils.jo_math import round_nearest
from src.utils.security_data import get_current_price

# todo make this an abstract class, implement it for IB and fio separately


def connect():
    ib_lib.util.startLoop()
    ib = ib_lib.IB()

    # ensure that we connect just once
    if not ib.isConnected():
        print('connecting')
        ib.connect('127.0.0.1', 7497, clientId=0, readonly=False)
        if ib.isConnected():
            ib.reqMarketDataType(1)
            print('connected')
        else:
            print('Error, try again or smthing')
    else:
        print('already connected')

    return ib


def get_cash_to_burn(ib):
    pos = ib.positions()

    # it is assumed that available funds are in eur
    # todo this assumption is wrong and should be generalized away
    cash_to_burn = [v for v in ib.accountValues() if v.tag == 'AvailableFunds' and v.currency == 'EUR'][0].value
    cash_to_burn = float(cash_to_burn)
    return cash_to_burn


def get_security_to_buy_count(free_cash):
    vwce_price = get_current_price('VWCE.DE')
    vwce_to_buy = math.floor(free_cash / vwce_price)
    # todo do not print in methods
    print(f'Going to buy {vwce_to_buy} VWCE at {vwce_price}')
    return vwce_to_buy


def execute_order(ib, direction, ticker, count, limit):
    if count < 1:
        raise ValueError("You can't buy zero of something")
    if direction != 'BUY' and direction != 'SELL':
        raise ValueError(f"Wrong param {direction} You can only BUY or SELL")

    ib_contract = ib_lib.Stock(ticker, "SMART", "EUR")
    order = ib_lib.LimitOrder('BUY', count, limit)
    trade = ib.placeOrder(ib_contract, order)

    # todo implement some sort of polling to wait until trade is executed (and throw if it isn't within some duration)
    ib.sleep(5)
    return trade.log


def run_strategy():
    ib = connect()
    free_cash = get_cash_to_burn(ib)
    wanted_stock = 'VWCE'  # todo take it from args or smthing
    wanted_stock_price = get_current_price('VWCE.DE')
    wanted_amount = math.floor((free_cash - 50) / wanted_stock_price)
    logs = execute_order(ib, 'BUY', wanted_stock, wanted_amount, round_nearest(wanted_stock_price * 1.03, 0.05))
    for log in logs:
        print(log.status)
    ib.disconnect()


if __name__ == "__main__":
    run_strategy()