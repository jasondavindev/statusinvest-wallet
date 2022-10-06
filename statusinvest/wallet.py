from datetime import datetime

import requests

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL

CONSOLIDATED_EARNINGS_ENDPOINT = '/AdmWallet/AssetEarningResult'
EARNINGS_BY_PERIOD_ENDPOINT = '/admwallet/allearningresult'

EARNING_PERIODS = {
    'last_month': -3,
    'current_month': -2,
    'all': 5,
}


class Earning:
    def __init__(self, row) -> None:
        self.code = row['code']
        self.name = row['name']
        self.date_com_raw = row['dateCom']
        self.date_com = datetime.fromisoformat(row['dateCom'])
        self.payment_date_raw = row['paymentDate']
        self.payment_date = datetime.fromisoformat(row['paymentDate'])
        self.quantity = row['quantity']
        self.unit_value = row['unitValue']
        self.total_value = row['totalValue']
        self.dividend_type_name = row['dividendTypeName']
        self.category_name = row['categoryName']


class WalletEarnings(Auth):
    def __init__(self) -> None:
        self.earnings = {}

    def consolidated_earnings(self):
        response = requests.post(
            url=f'{STATUS_INVEST_BASE_URL}{CONSOLIDATED_EARNINGS_ENDPOINT}',
            headers=self.auth_headers,
        )

        return response.json()

    def earnings_by_period(self, period='last_month'):
        data = {
            'groupView': 0,
            'type': EARNING_PERIODS[period],
            'dividendRankType': 0,
            'currency': 0,
        }

        response = requests.post(
            url=f'{STATUS_INVEST_BASE_URL}{EARNINGS_BY_PERIOD_ENDPOINT}',
            headers=self.auth_headers,
            data=data,
        )

        json_response = response.json()

        earnings_raw = json_response['data'][0]['list']
        total = json_response['data'][0]['total']

        earnings = [Earning(earning) for earning in earnings_raw]

        self.earnings[period] = {
            'total': total,
            'earnings': earnings,
        }

        return total, earnings
