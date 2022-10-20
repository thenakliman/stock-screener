from screener.exceptions.not_found import ReportDataNotFound
from screener.filters.stock.constants import REPORT_DATA_KEY, MISSED_CRITERIA_KEY, SATISFIED_CRITERIA_KEY


def find(key: str, metadata: dict):
    report = metadata.get(REPORT_DATA_KEY, {})
    _REPORT_KEY_TO_CALLBACK_MAPPINGS = {
        "name": lambda: report.get(key),
        "satisfied_strategies": lambda: metadata.get(key),
        "score": lambda: metadata.get(key),
        "debt_to_equity": lambda: report.get(key),
        "latest_debt_to_equity": lambda: report.get("latest_debt_to_equity", -1),
        "industry_debt_to_equity": lambda: report.get(key),
        "industry_price_to_book_value": lambda: report.get(key),
        "sector": lambda: report.get(key),
        "not_met_criterias": lambda: metadata.get(MISSED_CRITERIA_KEY),
        "met_criteria": lambda: metadata.get(SATISFIED_CRITERIA_KEY),
        "isinid": lambda: report.get(key),
        "asset_turnover": lambda: report.get(key),
        "cash_flows": lambda: report.get(key),
        "current_price": lambda: report.get(key),
        "current_ratio": lambda: report.get(key),
        "debt": lambda: report.get(key),
        "financial_year": lambda: report.get(key),
        "graham_number": lambda: report.get(key),
        "gross_margin": lambda: report.get(key),
        "incomes": lambda: report.get(key),
        "industry_pe": lambda: report.get(key),
        "less_than_maximum_price": lambda: report.get(key),
        "long_term_debts": lambda: report.get(key),
        "market_capital": lambda: report.get(key),
        "maximum_price": lambda: report.get(key),
        "minimum_price": lambda: report.get(key),
        "more_than_minimum_price": lambda: report.get(key),
        "net_sale": lambda: report.get(key),
        "new_issued_shares": lambda: report.get(key),
        "operating_cash_flow": lambda: report.get(key),
        "pe": lambda: report.get(key),
        "price_to_book": lambda: report.get(key),
        "return_on_assets": lambda: report.get(key),
        "tags": lambda: report.get(key),
        "total_issued_shares": lambda: report.get(key),
        "market_leader": lambda: report.get(key)
    }

    value_mapper = _REPORT_KEY_TO_CALLBACK_MAPPINGS.get(key)
    if value_mapper is None:
        raise ReportDataNotFound(data=key)

    return value_mapper()
