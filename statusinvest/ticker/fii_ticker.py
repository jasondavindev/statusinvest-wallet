class FIITicker:
    def __init__(
            self,
            *args,
            companyName: str = '',
            ticker: str = '',
            price: float = 0,
            dy: float = 0,
            p_vp: float = 0,
            **kwargs):
        self.companyName = companyName
        self.ticker = ticker
        self.price = price
        self.dy = dy
        self.p_vp = p_vp

    @staticmethod
    def new(data: dict):
        return FIITicker(**data)
