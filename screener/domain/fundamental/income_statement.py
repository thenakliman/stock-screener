class IncomeStatement:
    def __init__(self, financial_year: int, incomes: float, net_sale: float, expenses: float,
                 issued_shares: float, date_created: str, last_date_updated: str):
        self._financial_year = financial_year
        self._incomes = incomes
        self._net_sale = net_sale
        self._expense = expenses
        self._issued_shares = issued_shares
        self._date_created = date_created
        self._last_date_updated = last_date_updated

    def get_net_sales(self) -> float:
        return self._net_sale

    def get_gross_margin(self) -> float:
        return (self._net_sale - self._expense) / self._net_sale

    def get_net_income(self) -> float:
        return self._incomes

    def get_issued_shares(self) -> float:
        return self._issued_shares

    def get_financial_year(self) -> int:
        return self._financial_year
