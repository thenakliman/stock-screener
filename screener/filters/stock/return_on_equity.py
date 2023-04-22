from screener.common.constants import RETURN_ON_EQUITIES
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("return_on_equity")
def return_on_equity_filter_operation(stock, return_on_equity):
    return stock.get_return_on_equity(stock.find_financial_year_of_latest_results()) >= return_on_equity


@register_filter_operation("return_on_equity_is_greater_than_sector")
@register_enrich_operation("return_on_equity_is_greater_than_sector")
def sector_return_on_equity_filter_operation(stock):
    return stock.return_on_equity_is_greater_than_sector(stock.find_financial_year_of_latest_results())


@register_enrich_operation("return_on_equity_report")
def return_on_equity_filter_operation_enrich_operation(stock):
    stock.update_report_in_metadata({
        RETURN_ON_EQUITIES: [stock.get_return_on_equity(year) for year in
                             stock.get_financial_year_of_results()[:-1]]
    })
