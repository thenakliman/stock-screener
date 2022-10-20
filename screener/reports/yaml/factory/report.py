from typing import Optional, Dict, Union

from screener.factories import engine as engine_factory
from screener.reports.yaml.common import report_data_finder
from screener.reports.yaml.common.formatter import Formatter
from screener.reports.yaml.common.grouping import Grouper
from screener.reports.yaml.common.sorting import Sorter
from screener.reports.yaml.objects.index_report import IndexReport
from screener.reports.yaml.objects.sector_report import SectorReport
from screener.reports.yaml.objects.stock_report import Report

_DEFAULT_REPORT_FORMAT = [
    "name",
    "sector",
    "score",
    "current_price",
    "less_than_maximum_price",
    "more_than_minimum_price",
    "pe",
    "industry_pe",
    "market_capital",
    "minimum_price",
    "price_to_book",
    "maximum_price",
    "industry_debt_to_equity",
    "industry_price_to_book_value",
    "latest_debt_to_equity",
    "satisfied_strategies",
    {
        "score_card": [
            "net_sale",
            "incomes",
            "debt",
            "debt_to_equity",
            "long_term_debts",
            "pe",
            "industry_pe",
            "not_met_criterias",
            "met_criteria",
            "isinid",
            "market_leader",
            "financial_year",
            "asset_turnover",
            "cash_flows",
            "current_ratio",
            "financial_year",
            "graham_number",
            "gross_margin",
            "isinid",
            "market_capital",
            "name",
            "new_issued_shares",
            "operating_cash_flow",
            "price_to_book",
            "return_on_assets",
            "tags",
            "total_issued_shares",
            "name",
            "score",
            "sector",
            "more_than_minimum_price",
            "less_than_maximum_price"
        ]
    }
]


def get_formatter(output_format=None) -> Formatter:
    output_format = output_format or _DEFAULT_REPORT_FORMAT
    return Formatter(output_format, report_data_finder)


def get_grouper(group_by: str, keep_top_result: int, formatter: Optional[Formatter]) -> Grouper:
    formatter = formatter or get_formatter()
    return Grouper(group_by, report_data_finder, formatter, keep_top_result)


def get_sorter(ascending: bool = False, sorted_by: str = None) -> Sorter:
    return Sorter(report_data_finder, ascending, sorted_by)


def get_stock_report(config: Dict, output_file: str = None) -> Report:
    sorter = get_sorter(
        ascending=config["output"]["sort"]["ascending"],
        sorted_by=config["output"]["sort"]["by"],
    )
    formatter = get_formatter()
    grouper = get_grouper(
        config["output"].get("group_by"),
        config["output"].get("keep_top_results") or 3,
        formatter
    )
    operations = engine_factory.get_operations(config)
    return Report(
        output_file=output_file,
        sorter=sorter,
        grouper=grouper,
        operations=operations
    )


def get_report(report_type: str, config: Dict, output_file: str) -> Union[Report, SectorReport, IndexReport]:
    if report_type == "stock":
        return get_stock_report(config, output_file)
    if report_type == "index":
        return get_index_report(config, output_file)
    if report_type == "sector":
        return get_sector_report(config, output_file)

    raise ValueError("Invalid report type")


def get_index_report(config: Dict, output_file: str) -> IndexReport:
    return IndexReport(output_file=output_file,
                       ascending=config["output"]["sort"]["ascending"],
                       keep_top_results=config["output"]["sort"]["keep_top_results"],
                       sorted_by=config["output"]["sort"]["by"])


def get_sector_report(config: Dict, output_file: str) -> SectorReport:
    return SectorReport(output_file=output_file,
                        ascending=config.get("output", {}).get("sort", {}).get("ascending", False),
                        keep_top_results=config.get("output", {}).get("sort", {}).get("keep_top_results", 3000),
                        sorted_by=config.get("output", {}).get("sort", {}).get("by", "less_than_maximum"))
