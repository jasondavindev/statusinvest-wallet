from dataclasses import dataclass
from operator import itemgetter
from typing import Union

from slugify import slugify

from statusinvest.ticker.fii_ticker import FIITicker
from statusinvest.ticker.stock_ticker import StockTicker
from statusinvest.ticker.ticker import Ticker

DICT_ATTRIBUTES = [
    "code",
    "name",
    "unitValue",
    "price",
    "quantity",
    "sector",
    "subSector",
    "segment",
    "currentValue",
    "profitabilityPercent",
    "categoryPercent",
    "walletPercent",
    "categoryName"
]


@dataclass
class Asset:
    code: str
    name: str
    unitValue: float
    price: float
    quantity: float
    sector: str
    subSector: str
    segment: str
    currentValue: float
    profitabilityPercent: float
    categoryPercent: float
    walletPercent: float
    categoryName: str
    ticker: Union[StockTicker, FIITicker] = None
    cleanCategory: str = None

    @staticmethod
    def clear_category_name(category_name: str):
        slug = slugify(category_name)

        if slug == 'acoes':
            return 'acao'

        return slug

    @staticmethod
    def from_dict(data: dict):
        getter = itemgetter(*DICT_ATTRIBUTES)
        asset = Asset(*getter(data))
        asset.cleanCategory = Asset.clear_category_name(asset.categoryName)
        return asset

    def populate_ticker(self):
        ticker = Ticker().new(self.code, self.cleanCategory)
        self.ticker = ticker
        return self

    def get_metrics(self):
        if self.cleanCategory in ['acao', 'bdr']:
            return (
                round(self.ticker.p_l.actual, 2),
                round(self.ticker.p_vp.actual, 2),
                round(self.ticker.dy.actual, 2),
            )
        else:
            # fiis
            return (
                round(self.ticker.p_vp, 2),
                round(self.ticker.dy, 2),
            )
