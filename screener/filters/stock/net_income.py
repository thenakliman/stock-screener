from screener.common import constants
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("net_income")
@register_enrich_operation("net_income")
def net_income_filter_operation(stock, expected_increment):
    return stock.get_net_income(stock.find_financial_year_of_latest_results()) >= expected_increment


@register_filter_operation("positive_net_income")
@register_enrich_operation("positive_net_income")
def positive_net_income_filter_operation(stock):
    return stock.get_net_income(stock.find_financial_year_of_latest_results()) > 0


@register_filter_operation("increasing_net_income")
@register_enrich_operation("increasing_net_income")
def increasing_net_income(stock, for_years, expected_increment):
    return stock.net_income_increasing(stock.find_financial_year_of_latest_results(), for_years, expected_increment)


@register_enrich_operation("net_income_report")
def net_income_enrich_operation(stock):
    stock.update_report_in_metadata({
        constants.INCOMES: [stock.get_net_income(year) for year in stock.get_financial_year_of_results()]
    })
