import yfinance as yf


def get_current_price(ticker, yahoo=True):
    if yahoo:
        # todo handle none, wrong ticker etc
        # todo rate limit (at least 1s delay)
        t = yf.Ticker(ticker)
        return t.info["regularMarketPrice"]
    else:
        raise NotImplemented("This feature is not implemented yet")