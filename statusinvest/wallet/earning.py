from datetime import datetime

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
