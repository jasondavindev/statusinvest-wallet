from datetime import datetime

class Earning:
    def __init__(self, row) -> None:
        self.code = row['code']
        self.name = row['name']
        self.date_com_raw = row['dateCom']
        self.date_com = datetime.fromisoformat(row['dateCom'])
        self.payment_date_raw = row.get('paymentDate')
        self.payment_date = datetime.fromisoformat(row.get('paymentDate', '1900-01-01'))
        self.quantity = round(row['quantity'], 2)
        self.unit_value = round(row['unitValue'], 2)
        self.total_value = round(row['totalValue'], 2)
        self.dividend_type_name = row['dividendTypeName']
        self.category_name = row['categoryName']
