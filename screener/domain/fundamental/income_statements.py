from typing import List, Tuple, Dict

from screener.domain.fundamental.income_statement import IncomeStatement
from screener.exceptions.not_found import IncomeStatementNotFound


class IncomeStatements:
    def __init__(self, income_statements: List[IncomeStatement]):
        self._income_statements = income_statements

    def _find_income_statement(self, year: int) -> IncomeStatement:
        for income_statement in self._income_statements:
            if income_statement.get_financial_year() == year:
                return income_statement

        raise IncomeStatementNotFound(year=year)

    def increasing_gross_margin(self, year: int) -> bool:
        gross_margin_in_given_year = self._find_income_statement(year).get_gross_margin()
        gross_margin_in_previous_year = self._find_income_statement(year - 1).get_gross_margin()
        return gross_margin_in_given_year > gross_margin_in_previous_year

    def get_gross_margin(self, year) -> float:
        return self._find_income_statement(year).get_gross_margin()

    def get_net_income(self, year: int) -> float:
        return self._find_income_statement(year).get_net_income()

    def net_income_increasing(self, year: int, for_years: int, expected_increment: float) -> bool:
        previous_year = year
        for _ in range(for_years):
            current_year = previous_year
            previous_year = current_year - 1
            net_income_in_given_year = self._find_income_statement(current_year).get_net_income()
            net_income_in_previous_year = self._find_income_statement(previous_year).get_net_income()
            if net_income_in_given_year < net_income_in_previous_year * (1 + expected_increment / 100.0):
                return False

        return True

    def get_issued_shares(self, year: int) -> float:
        return self._find_income_statement(year).get_issued_shares()

    def new_shares_issued(self, year: int) -> bool:
        return self.get_new_shares_issued(year) > 0

    def get_new_shares_issued(self, year: int) -> float:
        shares_in_given_year = self._find_income_statement(year).get_issued_shares()
        shares_in_previous_year = self._find_income_statement(year - 1).get_issued_shares()
        return shares_in_given_year - shares_in_previous_year * 1.000055

    def get_net_sales(self, year: int) -> float:
        return self._find_income_statement(year).get_net_sales()

    def net_sale_increasing(self, year: int, for_years: int, increase_in_percentage: float) -> bool:
        previous_year = year
        for _ in range(for_years):
            current_year = previous_year
            previous_year = current_year - 1
            net_sales_in_given_year = self._find_income_statement(current_year).get_net_sales()
            net_sales_in_previous_year = self._find_income_statement(previous_year).get_net_sales()
            if net_sales_in_given_year < net_sales_in_previous_year * (1 + increase_in_percentage / 100.0):
                return False

        return True

    def net_sale_increased_by(self, year: int, in_years: int, increase_in_percentage: float):
        net_sales_in_given_year = self._find_income_statement(year).get_net_sales()
        net_sales_in_previous_year = self._find_income_statement(year - in_years).get_net_sales()
        return net_sales_in_given_year >= (net_sales_in_previous_year * (1 + increase_in_percentage / 100))

    def get_latest_financial_year_of_result(self) -> int:
        return max(self.get_financial_year_of_results(), default=1985)

    def get_financial_year_of_results(self) -> Tuple[int]:
        return tuple(income_statement.get_financial_year() for income_statement in self._income_statements)

    def net_sale_compare_to_sector(self, increase_in_percentage: int, yearwise_increase_sales_ratio: List[Dict]):
        for sale in yearwise_increase_sales_ratio:
            current_year = sale.get("year")
            previous_year = current_year - 1
            net_sales_in_given_year = self._find_income_statement(current_year).get_net_sales()
            net_sales_in_previous_year = self._find_income_statement(previous_year).get_net_sales()
            if net_sales_in_given_year < \
                    net_sales_in_previous_year * ((increase_in_percentage + sale.get("increase") + 100)/100):
                return False

        return True
