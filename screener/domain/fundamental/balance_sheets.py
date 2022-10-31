from typing import List, Tuple

from screener.domain.fundamental.balance_sheet import BalanceSheet
from screener.exceptions.not_found import BalanceSheetNotFound


class BalanceSheets:
    def __init__(self, balance_sheets: List[BalanceSheet]):
        self._balance_sheets = balance_sheets

    def get_latest_financial_year_of_result(self) -> int:
        return max(self.get_financial_year_of_results(), default=1985)

    def _find_balance_sheet_for_year(self, year: int) -> BalanceSheet:
        for balance_sheet in self._balance_sheets:
            if balance_sheet.get_financial_year() == year:
                return balance_sheet

        raise BalanceSheetNotFound(year=year)

    def increasing_current_ratio(self, year: int) -> bool:
        given_year_balance_sheet = self._find_balance_sheet_for_year(year)
        previous_year_balance_sheet = self._find_balance_sheet_for_year(year - 1)
        return given_year_balance_sheet.get_current_ratio() >= previous_year_balance_sheet.get_current_ratio()

    def get_current_ratio(self, year) -> float:
        return self._find_balance_sheet_for_year(year).get_current_ratio()

    def get_total_debt(self, year) -> float:
        return self._find_balance_sheet_for_year(year).get_total_debt()

    def get_long_term_debts(self, year) -> float:
        return self._find_balance_sheet_for_year(year).get_long_term_debts()

    def get_debt_to_equity_ratio(self, year) -> float:
        return self._find_balance_sheet_for_year(year).get_debt_to_equity_ratio()

    def decreasing_long_term_debt_ratio_by_year(self, year) -> bool:
        given_year_balance_sheet = self._find_balance_sheet_for_year(year)
        previous_year_balance_sheet = self._find_balance_sheet_for_year(year - 1)
        return given_year_balance_sheet.get_long_term_debts() <= previous_year_balance_sheet.get_long_term_debts()

    def get_asset(self, year: int) -> float:
        return self._find_balance_sheet_for_year(year).get_total_asset()

    def get_financial_year_of_results(self) -> Tuple[int]:
        return tuple(balance_sheet.get_financial_year() for balance_sheet in self._balance_sheets)
