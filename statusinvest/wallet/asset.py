from dataclasses import dataclass
from operator import itemgetter

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

    @staticmethod
    def from_dict(data: dict):
        getter = itemgetter(*DICT_ATTRIBUTES)
        # TODO: set ticker using statusinvest.ticker.Ticker
        return Asset(*getter(data))
