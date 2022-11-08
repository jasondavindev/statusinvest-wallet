import requests

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL
from statusinvest.wallet.earning import Earning

CONSOLIDATED_EARNINGS_ENDPOINT = '/AdmWallet/AssetEarningResult'
EARNINGS_BY_PERIOD_ENDPOINT = '/admwallet/allearningresult'

EARNING_PERIODS = {
    'last_month': -3,
    'current_month': -2,
    'all': 5,
}


class WalletEarnings:
    def __init__(self) -> None:
        self.earnings = {}

    def consolidated_earnings(self):
        response = requests.post(
            url=f'{STATUS_INVEST_BASE_URL}{CONSOLIDATED_EARNINGS_ENDPOINT}',
            headers=Auth.from_env().auth_headers,
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
            headers=Auth.from_env().auth_headers,
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
