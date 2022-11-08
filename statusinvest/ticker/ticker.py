from functools import cached_property

import requests

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL
from statusinvest.ticker.fii_ticker import FIITicker
from statusinvest.ticker.stock_ticker import StockTicker
from statusinvest.utils.singleton import SingletonMeta

ADVANCED_URL = '/category/advancedsearchresult'


class Ticker(metaclass=SingletonMeta):
    def __init__(self) -> None:
        print('Building tickers')
        self.fiis = None

    @cached_property
    def get_fiis(self):
        search_params = '?search={}&CategoryType=2'

        print('Searching FIIs')

        response = requests.get(
            f'{STATUS_INVEST_BASE_URL}{ADVANCED_URL}{search_params}',
            headers=Auth.from_env().auth_headers,
        )

        data = response.json()

        fiis = dict(map(lambda x: (x['ticker'], FIITicker.new(x)), data))

        self.fiis = fiis
        return self.fiis

    def new(self, ticker: str, category: str):
        if category in ['acao', 'bdr']:
            print(f'Building Stock ticker={ticker}')
            return StockTicker.new(ticker, category)

        if category == 'fiis':
            return self.get_fiis[ticker]


if __name__ == '__main__':
    ticker = Ticker()
    print(ticker.new('bbas3', 'acao'))
