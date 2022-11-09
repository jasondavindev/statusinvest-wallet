import csv
from operator import attrgetter

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
    earnings = {}

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

        earnings = list(map(lambda earning: Earning(earning), earnings_raw))

        self.earnings[period] = earnings

    def export(self):
        with open('data/earnings.csv', 'w') as csv_file:
            fields = [
                'period',
                'code',
                'name',
                'date_com',
                'payment_date',
                'quantity',
                'unit_value',
                'total_value',
                'dividend_type_name',
                'category_name',
            ]

            writer = csv.DictWriter(csv_file, fields)
            writer.writeheader()
            getter = attrgetter(*fields[1:])

            for period, earnings in self.earnings.items():
                rows = map(
                    lambda earning: dict(
                        zip(fields, (period,) + getter(earning))
                    ), earnings
                )
                sorted_rows = sorted(rows, key=lambda row: row['payment_date'])
                writer.writerows(sorted_rows)


if __name__ == '__main__':
    wallet = WalletEarnings()
    wallet.earnings_by_period()
    wallet.export()
