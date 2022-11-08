import csv
from operator import attrgetter, itemgetter
from typing import Dict, List

import requests
from slugify import slugify

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL
from statusinvest.wallet.asset import Asset

ASSETS_URL = '/AdmWallet/PatrimonyAssetCompleteResult'


class Assets:
    assets: Dict[str, List[Asset]]

    def get_assets(self):
        auth = Auth.from_env()

        print('Searching Complete assets')

        response = requests.post(
            url=f'{STATUS_INVEST_BASE_URL}{ASSETS_URL}',
            headers=auth.auth_headers,
        )

        data = response.json()
        self.format_response(data)

    def format_response(self, data):
        self.assets = {
            slugify(category['categoryName']): list(
                map(Asset.from_dict, category['assets'])
            ) for category in data['data']['list']
        }

    def export(self, category='acao'):
        assets = self.assets[category if category != 'acao' else 'acoes']

        fields = [
            'code',
            'name',
            'unitValue',
            'price',
            'quantity',
            'segment',
        ]

        fields_getter = attrgetter(*fields)

        extra_fields = ['pL', 'pVP', 'dY'] if category in ['acao', 'bdr'] \
            else ['pVP', 'dY']

        sort_getter = itemgetter(*extra_fields)
        fields += extra_fields

        assets_with_ticker = map(lambda asset: asset.populate_ticker(), assets)

        assets_to_dict = map(lambda asset: dict(
            zip(fields, fields_getter(asset) + asset.get_metrics())
        ), assets_with_ticker)

        sorted_assets = sorted(assets_to_dict, key=sort_getter)

        with open(f'data/wallet_{category}.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fields)
            writer.writeheader()
            [writer.writerow(row) for row in sorted_assets]


if __name__ == '__main__':
    assets = Assets()
    assets.get_assets()
    assets.export('acoes')
