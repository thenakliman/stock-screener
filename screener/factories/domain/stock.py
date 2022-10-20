from typing import Dict, List

from screener.common import constants
from screener.common.constants import BALANCE_SHEET, PROFIT_LOSS_STATEMENT, CASH_FLOWS, FINANCIAL_RATIOS
from screener.domain.technical.day_value import DayValue
from screener.domain.technical.historical_prices import HistoricalValues
from screener.domain.fundamental.balance_sheet import BalanceSheet
from screener.domain.fundamental.balance_sheets import BalanceSheets
from screener.domain.fundamental.cash_flow import CashFlow
from screener.domain.fundamental.cash_flows import CashFlows
from screener.domain.fundamental.financial_ratio import FinancialRatio
from screener.domain.fundamental.financial_ratios import FinancialRatioV2
from screener.domain.fundamental.income_statement import IncomeStatement
from screener.domain.fundamental.income_statements import IncomeStatements
from screener.domain.fundamental.stock import Stock


def get_historical_prices(values: List[dict],
                          date_extractor=lambda value: value.get("date"),
                          value_extractor=lambda value: value.get("value"),
                          low_extractor=lambda value: value.get("low"),
                          high_extractor=lambda value: value.get("high"),
                          open_value_extractor=lambda value: value.get("open"),
                          volume_extractor=lambda value: value.get("volume")) -> List[DayValue]:
    return [DayValue(date_extractor(value),
                     value_extractor(value),
                     open_value_extractor(value),
                     low_extractor(value),
                     high_extractor(value),
                     volume_extractor(value)) for value in values]


def get_stock(stock_details: dict) -> Stock:
    historical_prices_as_dict = stock_details.get(constants.HISTORICAL_PRICES, [])
    stock_details[constants.HISTORICAL_PRICES] = HistoricalValues(get_historical_prices(historical_prices_as_dict))
    return Stock(
        stock_details,
        BalanceSheets(get_balance_sheet(stock_details.get(BALANCE_SHEET, []))),
        IncomeStatements(get_income_statement(stock_details.get(PROFIT_LOSS_STATEMENT, []))),
        CashFlows(get_cash_flow(stock_details.get(CASH_FLOWS, []))),
        FinancialRatioV2(get_financial_ratio(stock_details.get(FINANCIAL_RATIOS, [])))
    )


def get_financial_ratio(financial_ratios: Dict) -> List[FinancialRatio]:
    return [FinancialRatio(
        current_ratio=financial_ratio.get("current_ratio"),
        gross_margin=financial_ratio.get("gross_margin"),
        asset_turnover_ratio=financial_ratio.get("asset_turnover_ratio"),
        return_on_asset=financial_ratio.get("return_on_asset"),
        financial_year=financial_ratio.get("financial_year"),
        date_created=financial_ratio.get("date_created"),
        last_date_updated=financial_ratio.get("last_date_updated")) for financial_ratio in financial_ratios
    ]


def get_cash_flow(cash_flows: Dict) -> List[CashFlow]:
    return [CashFlow(
        financial_year=cash_flow.get("financial_year"),
        cash_flow_from_operating_activities=cash_flow.get("cash_flow_from_operating_activities"),
        date_created=cash_flow.get("date_created"),
        last_date_updated=cash_flow.get("last_date_updated")) for cash_flow in cash_flows
    ]


def get_income_statement(income_statements: Dict) -> List[IncomeStatement]:
    return [IncomeStatement(
        financial_year=income_statement.get("financial_year"),
        incomes=income_statement.get("income"),
        net_sale=income_statement.get("net_sale"),
        expenses=income_statement.get("total_expense"),
        issued_shares=income_statement.get("issued_shares"),
        date_created=income_statement.get("date_created"),
        last_date_updated=income_statement.get("last_date_updated")) for income_statement in income_statements
    ]


def get_balance_sheet(balance_sheets: Dict) -> List[BalanceSheet]:
    return [BalanceSheet(
        financial_year=balance_sheet.get("financial_year"),
        total_current_liability=balance_sheet.get("total_current_liability"),
        total_current_asset=balance_sheet.get("total_current_asset"),
        total_non_current_asset=balance_sheet.get("total_non_current_asset"),
        total_shareholders_funds=balance_sheet.get("total_shareholders_fund"),
        total_asset=balance_sheet.get("total_asset"),
        long_term_borrowings=balance_sheet.get("long_term_borrowing"),
        short_term_borrowings=balance_sheet.get("short_term_borrowings"),
        date_created=balance_sheet.get("date_created"),
        last_date_updated=balance_sheet.get("last_date_updated")) for balance_sheet in balance_sheets
    ]
