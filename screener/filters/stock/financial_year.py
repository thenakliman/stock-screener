from screener.common.year import is_latest_financial_year
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("latest_financial_year")
@register_enrich_operation("latest_financial_year")
def latest_financial_year_filter_operation(stock):
    return is_latest_financial_year(stock.find_financial_year_of_latest_results())


@register_enrich_operation("latest_financial_year_report")
def latest_financial_year_enrich_operation(stock):
    stock.update_report_in_metadata({
        "financial_year": stock.find_financial_year_of_latest_results()
    })
