from typing import List, Tuple

from screener.domain.fundamental.financial_ratio import FinancialRatio
from screener.exceptions.not_found import FinancialRatioNotFound


class FinancialRatioV2:
    def __init__(self, financial_ratios: List[FinancialRatio]):
        self._financial_ratios = financial_ratios

    def _find_balance_sheet_for_year(self, year: int) -> FinancialRatio:
        for financial_ratio in self._financial_ratios:
            if financial_ratio.get_financial_year() == year:
                return financial_ratio

        raise FinancialRatioNotFound(year=year)

    def increasing_current_ratio(self, year: int) -> bool:
        return (
                self._find_balance_sheet_for_year(year).get_current_ratio() >
                self._find_balance_sheet_for_year(year - 1).get_current_ratio()
        )

    def get_current_ratio(self, year: int) -> float:
        return self._find_balance_sheet_for_year(year).get_current_ratio()

    def increasing_gross_margin(self, year: int) -> bool:
        return (
                self._find_balance_sheet_for_year(year).get_gross_margin() >
                self._find_balance_sheet_for_year(year - 1).get_gross_margin()
        )

    def get_return_on_asset(self, year: int) -> float:
        return self._find_balance_sheet_for_year(year).get_return_on_asset()

    def increasing_asset_turnover_ratio(self, year: int) -> bool:
        return (
                self._find_balance_sheet_for_year(year).get_asset_turnover() >
                self._find_balance_sheet_for_year(year - 1).get_asset_turnover()
        )

    def get_financial_year_of_results(self) -> Tuple[int]:
        return tuple(financial_ratio.get_financial_year() for financial_ratio in self._financial_ratios)
