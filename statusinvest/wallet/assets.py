import requests
from slugify import slugify

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL
from statusinvest.wallet.asset import Asset

ASSETS_URL = '/AdmWallet/PatrimonyAssetCompleteResult'


class Assets:
    def get_assets(self):
        auth = Auth.from_env()

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


if __name__ == '__main__':
    assets = Assets()
    assets.get_assets()
    print(assets.assets)
