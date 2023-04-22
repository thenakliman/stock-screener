class BalanceSheet:
    def __init__(self,
                 financial_year: int,
                 total_current_liability: float,
                 total_current_asset: float,
                 total_non_current_asset: float,
                 total_shareholders_funds: float,
                 total_asset: float,
                 long_term_borrowings: float,
                 short_term_borrowings: float,
                 date_created: str,
                 last_date_updated: str):
        self._financial_year = financial_year
        self._total_current_liability = total_current_liability
        self._total_current_asset = total_current_asset
        self._total_non_current_asset = total_non_current_asset
        self._total_shareholders_funds = total_shareholders_funds
        self._total_asset = total_asset
        self._long_term_borrowings = long_term_borrowings
        self._short_term_borrowings = short_term_borrowings
        self._date_created = date_created
        self._last_date_updated = last_date_updated

    def get_total_assets(self) -> float:
        return self._total_asset

    def get_current_ratio(self) -> float:
        return self._total_current_asset / self._total_current_liability

    def get_long_term_debts(self) -> float:
        return self._long_term_borrowings

    # FIXME: fix it when we have current and non current libailities
    def get_debt_to_equity_ratio(self) -> float:
        return self.get_total_debt() / self._total_shareholders_funds

    def get_shareholders_fund(self) -> float:
        return self._total_shareholders_funds

    def get_total_debt(self) -> float:
        return self._short_term_borrowings + self._long_term_borrowings

    def get_total_asset(self) -> float:
        return self._total_asset

    def get_financial_year(self) -> int:
        return self._financial_year
