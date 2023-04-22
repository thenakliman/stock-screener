import copy
from typing import List

from screener.common import constants, date
from screener.common.constants import ISINID
from screener.common.u_dict import merge_dict
from screener.domain.fundamental.balance_sheets import BalanceSheets
from screener.domain.fundamental.cash_flows import CashFlows
from screener.domain.fundamental.financial_ratios import FinancialRatioV2
from screener.domain.fundamental.income_statements import IncomeStatements
from screener.domain.technical.day_value import DayValue
from screener.exceptions.not_found import DataNotFound, CurrentPriceNotFound
from screener.filters.stock.constants import (
    REPORT_DATA_KEY,
    MISSED_CRITERIA_KEY,
    SATISFIED_CRITERIA_KEY,
    SCORE_KEY,
    ReportKeys
)
from screener.filters.stock.exception import log_exception


class Stock:
    def __init__(self, stock_detail, balance_sheets: BalanceSheets, income_statements: IncomeStatements,
                 cash_flows: CashFlows, financial_ratios: FinancialRatioV2):
        self._id = stock_detail["_id"]
        self._industry_pe = stock_detail[constants.INDUSTRY_PE]
        self._pe = stock_detail[constants.PE]
        self._market_capital_free_float = stock_detail[constants.MARKET_CAPITAL_FULL]
        self._isinid = stock_detail[ISINID]
        self._name = stock_detail[constants.NAME]
        self._put_to_call = stock_detail[constants.PUT_TO_CALL]
        self._eps_twelve_month = stock_detail.get(constants.EPS_TWELVE_MONTH, 0)
        self._group = stock_detail[constants.GROUP]
        self._face_value = stock_detail[constants.FACE_VALUE]
        self._dividend_percentage = stock_detail[constants.DIVIDEND_PERCENTAGE]
        self._book_value = stock_detail[constants.BOOK_VALUE]
        self._cash_eps = stock_detail[constants.CASH_EPS]
        self._current_price = stock_detail[constants.PRICE]
        self._industry = stock_detail[constants.INDUSTRY]
        self._sub_industry = stock_detail[constants.SUB_INDUSTRY]
        self._historical_prices = stock_detail[constants.HISTORICAL_PRICES]
        self._tags = stock_detail.get(constants.TAGS, [])
        self._active = stock_detail.get(constants.ACTIVE)
        self._sector_name = stock_detail.get(constants.SECTOR)
        self._sector = None
        self._metadata = {}
        self._market_leader = False
        self._balance_sheets = balance_sheets
        self._income_statements = income_statements
        self._financial_ratios = financial_ratios
        self._cash_flows = cash_flows
        self._date_created = stock_detail.get(constants.DATE_CREATED, date.today())
        self._last_date_updated = stock_detail.get(constants.LAST_DATE_UPDATED, date.today())

    @log_exception
    def get_price_to_book_value(self):
        return self._current_price / (self._book_value + 0.01)

    @log_exception
    def get_industry_price_to_book_value(self) -> float:
        return self._sector.get_price_to_book_value()

    @log_exception
    def price_to_book_less_than_industry(self, by_percentage):
        return self._sector.get_price_to_book_value() * (100 - by_percentage) > self.get_price_to_book_value() * 100

    @log_exception
    def mark_market_leader(self) -> None:
        self._market_leader = True

    @log_exception
    def market_leader(self) -> bool:
        return self._market_leader

    @log_exception
    def find_financial_year_of_latest_balance_sheet(self) -> int:
        return self._balance_sheets.get_latest_financial_year_of_result()

    @log_exception
    def find_financial_year_of_latest_results(self) -> int:
        return min([
            self._cash_flows.get_latest_financial_year_of_result(),
            self._income_statements.get_latest_financial_year_of_result(),
            self._balance_sheets.get_latest_financial_year_of_result()
        ])

    @log_exception
    def has_tags(self, tags):
        lower_case_required_tags = [tag.lower() for tag in tags]
        for tag in self._tags:
            lower_cased_tag = tag.lower()
            if lower_cased_tag in lower_case_required_tags:
                return True

        return False

    @log_exception
    def get_tags(self):
        return copy.deepcopy(self._tags)

    @log_exception
    def get_pe(self):
        return self._pe

    @log_exception
    def pe_is_less_than_sector_pe(self):
        return self._pe <= self._sector.get_pe()

    @log_exception
    def get_isinid(self):
        return self._isinid

    @log_exception
    def get_industry_pe(self):
        return self._industry_pe

    @log_exception
    def get_market_capital(self):
        return self._market_capital_free_float

    @log_exception
    def number_of_days_stock_in_market(self):
        return self._historical_prices.number_of_days_stock_in_market()

    @log_exception
    def minimum_price_in_given_days(self, days: int) -> float:
        return self._historical_prices.minimum_price_in_given_days(days)

    @log_exception
    def maximum_price_in_given_days(self, days):
        return self._historical_prices.maximum_price_in_given_days(days)

    @log_exception
    def get_current_price(self) -> float:
        price = self._historical_prices.get_current_price()
        if price is None:
            raise CurrentPriceNotFound(isinid=self._isinid)

        return float(price)

    @log_exception
    def get_historical_prices(self):
        return self._historical_prices.to_dict()

    @log_exception
    def get_company_name(self):
        return self._name

    @log_exception
    def get_group(self):
        return self._group

    @log_exception
    def increasing_current_ratio(self, year: int) -> bool:
        if self._balance_sheets is None:
            return self._financial_ratios.increasing_current_ratio(year)

        return self._balance_sheets.increasing_current_ratio(year)

    @log_exception
    def current_ratio_is_greater_than_sector(self, year: int):
        return self.get_current_ratio(year) >= self._sector.get_current_ratio()

    @log_exception
    def get_current_ratio(self, year: int) -> float:
        if self._balance_sheets is None:
            return self._financial_ratios.get_current_ratio(year)

        return self._balance_sheets.get_current_ratio(year)

    @log_exception
    def has_latest_data(self, last_date_when_market_opened: str) -> bool:
        return last_date_when_market_opened == self._historical_prices.get_date_of_latest_available_price()

    @log_exception
    def get_date_of_latest_available_price(self):
        return self._historical_prices.get_date_of_latest_available_price()

    @log_exception
    def get_graham_number(self, maximum_allowed_eps=15, maximum_allowed_book_value=1.5):
        return (self._book_value *
                self._eps_twelve_month *
                maximum_allowed_eps *
                maximum_allowed_book_value) ** 0.5

    @log_exception
    def add_prices(self, prices: List[DayValue]):
        self._historical_prices.add_latest_price(prices)

    @log_exception
    def get_debt(self, year: int):
        return self._balance_sheets.get_total_debt(year)

    @log_exception
    def decreasing_long_term_debt_ratio_by_year(self, year: int) -> bool:
        return self._balance_sheets.decreasing_long_term_debt_ratio_by_year(year)

    @log_exception
    def get_long_term_debts(self, year: int):
        return self._balance_sheets.get_long_term_debts(year)

    @log_exception
    def get_debt_to_equity_ratio(self, year: int) -> float:
        try:
            return self._balance_sheets.get_debt_to_equity_ratio(year)
        except Exception as e:
            print("failed to get debt to equity ratio ", self._isinid, e)
        return -1

    @log_exception
    def get_sector_debt_to_equity(self) -> float:
        return self._sector.get_debt_to_equity()

    @log_exception
    def debt_to_equity_is_less_than_industry(self, by_percentage: float) -> float:
        return (
                self._sector.get_debt_to_equity() * (100 - by_percentage) >=
                100 * self.get_debt_to_equity_ratio(self.find_financial_year_of_latest_results())
        )

    @log_exception
    def increasing_gross_margin(self, year: int) -> bool:
        if self._income_statements is None:
            return self._financial_ratios.increasing_gross_margin(year)

        return self._income_statements.increasing_gross_margin(year)

    @log_exception
    def gross_margin_is_greater_than_sector(self, year: int):
        return self.get_gross_margin(year) >= self._sector.get_gross_margin()

    @log_exception
    def get_gross_margin(self, year: int) -> float:
        return self._income_statements.get_gross_margin(year)

    @log_exception
    def get_net_income(self, year: int) -> float:
        return self._income_statements.get_net_income(year)

    @log_exception
    def net_income_increasing(self, year: int, for_years: int, expected_increment: float) -> bool:
        return self._income_statements.net_income_increasing(year, for_years, expected_increment)

    @log_exception
    def get_issued_shares(self, year: int):
        return self._income_statements.get_issued_shares(year)

    @log_exception
    def new_shares_issued(self, year: int):
        return self._income_statements.new_shares_issued(year)

    @log_exception
    def get_new_issued_shares(self, year: int):
        return self._income_statements.get_new_shares_issued(year)

    @log_exception
    def increasing_return_on_asset(self, year: int):
        if self._income_statements is None:
            return self._financial_ratios.get_return_on_asset(year)

        return self.calculate_return_on_asset(year) >= self.calculate_return_on_asset(year - 1)

    @log_exception
    def calculate_return_on_asset(self, year: int):
        net_incomes = self._income_statements.get_net_income(year)
        assets = self._balance_sheets.get_asset(year - 1)
        return net_incomes / (assets + 0.01)

    @log_exception
    def get_financial_year_of_results(self) -> List[int]:
        return sorted(list(
            set(self._balance_sheets.get_financial_year_of_results()).intersection(
                set(self._income_statements.get_financial_year_of_results())).intersection(
                set(self._cash_flows.get_financial_year_of_results()))
        ), reverse=True)[:7]

    @log_exception
    def return_on_asset_is_greater_than_sector(self, year: int):
        return self.calculate_return_on_asset(year) >= self._sector.get_return_on_asset()

    @log_exception
    def get_net_sales_for_year(self, year: int):
        return self._income_statements.get_net_sales(year)

    @log_exception
    def net_sale_increasing(self, year: int, for_years: int, increase_in_percentage: float = 0.1):
        return self._income_statements.net_sale_increasing(year, for_years, increase_in_percentage)

    @log_exception
    def net_sale_compare_to_sector(self, for_years: int, increase_in_percentage: int = 0.1):
        increase_in_sales = self._sector.increase_in_sales(for_years)
        return self._income_statements.net_sale_compare_to_sector(increase_in_percentage, increase_in_sales)

    @log_exception
    def net_sale_increased_by(self, year: int, in_years: int, increase_in_percentage: float = 0.1) -> bool:
        return self._income_statements.net_sale_increased_by(year, in_years, increase_in_percentage)

    @log_exception
    def increasing_asset_turnover_ratio(self, year: int):
        if self._income_statements is None:
            return self._financial_ratios.increasing_asset_turnover_ratio(year)

        return self.calculate_asset_turnover(year) >= self.calculate_asset_turnover(year - 1)

    @log_exception
    def asset_turnover_is_greater_than_sector(self, year: int):
        return self.calculate_asset_turnover(year) >= self._sector.get_asset_turnover()

    @log_exception
    def calculate_asset_turnover(self, year: int):
        net_sales = self._income_statements.get_net_sales(year)
        previous_year_assets = self._balance_sheets.get_asset(year - 1)
        return net_sales / (previous_year_assets + 0.01)

    @log_exception
    def positive_cash_flow(self, year: int):
        try:
            return self._cash_flows.positive_cash_flow(year)
        except DataNotFound:
            print(f"Data not found for the calculations of operating cash flow ratio for {self._isinid}")

        return False

    @log_exception
    def get_operating_cash_flow_ratio(self, year: int):
        try:
            return self._cash_flows.get_cash_flow(year) / (self._balance_sheets.get_asset(year - 1) + 0.01)
        except DataNotFound:
            print(f"Data not found for the calculations of operating cash flow ratio for {self._isinid}")

        return -1

    @log_exception
    def update_cash_flow(self, cash_flow):
        self._cash_flows = cash_flow

    @log_exception
    def update_sector(self, sector):
        self._sector = sector

    @log_exception
    def update_balance_sheets(self, balance_sheet):
        self._balance_sheets = balance_sheet

    @log_exception
    def update_profit_loss_statement(self, profit_loss_statement):
        self._income_statements = profit_loss_statement

    @log_exception
    def update_financial_ratios(self, financial_ratios):
        self._financial_ratios = financial_ratios

    @log_exception
    def get_sector_name(self):
        return self._sector_name

    @log_exception
    def find_cash_flow(self, year: int):
        return self._cash_flows.get_cash_flow(year)

    @log_exception
    def cash_flow_greater_than_net_income(self, year: int):
        return self._cash_flows.get_cash_flow(year) >= self.get_net_income(year)

    @log_exception
    def add_metadata(self, property_name, value):
        self._metadata[property_name] = value

    @log_exception
    def remove_metadata(self, property_name):
        del self._metadata[property_name]

    @log_exception
    def cleanup_metadata(self):
        self._metadata.clear()

    @log_exception
    def _update_operation_status(self, key, operation_name):
        if key in self._metadata:
            if operation_name not in self._metadata[key]:
                self._metadata[key].append(operation_name)
        else:
            self._metadata[key] = [operation_name]

    @log_exception
    def update_success_operation_status(self, operation_name):
        self._update_operation_status(SATISFIED_CRITERIA_KEY, operation_name)

    @log_exception
    def update_failed_operation_status(self, operation_name):
        self._update_operation_status(MISSED_CRITERIA_KEY, operation_name)

    @log_exception
    def update_satisfied_strategy(self, flow_name):
        if ReportKeys.SATISFIED_STRATEGIES in self._metadata:
            self._metadata[ReportKeys.SATISFIED_STRATEGIES].append(flow_name)
        else:
            self._metadata[ReportKeys.SATISFIED_STRATEGIES] = [flow_name]

    @log_exception
    def update_score_by(self, score: float) -> None:
        if SCORE_KEY in self._metadata:
            self._metadata[SCORE_KEY] += score
        else:
            self._metadata[SCORE_KEY] = score

    @log_exception
    def update_score_to(self, score: float) -> None:
        self._metadata[SCORE_KEY] = score

    @log_exception
    def update_report_in_metadata(self, metadata):
        if REPORT_DATA_KEY in self._metadata:
            merge_dict(self._metadata[REPORT_DATA_KEY], metadata)
        else:
            self._metadata[REPORT_DATA_KEY] = metadata

    @log_exception
    def get_report_from_metadata(self):
        return self._metadata[REPORT_DATA_KEY]

    @log_exception
    def get_metadata(self):
        return self._metadata

    @log_exception
    def get_last_date_updated(self):
        return self._last_date_updated

    @log_exception
    def add_tag(self, tag) -> None:
        if tag not in self._tags:
            self._tags.append(tag)

    def get_industry(self) -> str:
        return self._industry

    def get_sub_industry(self) -> str:
        return self._sub_industry

    def get_sector(self):
        return self._sector

    def get_return_on_equity(self, year: int) -> float:
        return self._income_statements.get_net_income(year) / (0.01 + self._balance_sheets.get_shareholders_fund(year))

    def return_on_equity_is_greater_than_sector(self, year: int) -> float:
        return self.get_return_on_equity(year) > self._sector.get_return_on_equity()
