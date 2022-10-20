from screener.common import constants
from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("operating_cash_flow")
@register_enrich_operation("operating_cash_flow")
def operating_cash_flow_filter_operation(stock):
    return stock.positive_cash_flow(stock.find_financial_year_of_latest_results())


@register_enrich_operation("operating_cash_flow_report")
def operating_cash_flow_enrich_operation(stock):
    stock.update_report_in_metadata({
        "operating_cash_flow": [stock.get_operating_cash_flow_ratio(year) for year in
                                stock.get_financial_year_of_results()[:-1]]
    })


@register_filter_operation("cash_flow_greater_than_net_income")
@register_enrich_operation("cash_flow_greater_than_net_income")
def cash_flow_greater_than_net_income_filter_operation(stock):
    return stock.cash_flow_greater_than_net_income(stock.find_financial_year_of_latest_results())


@register_enrich_operation("cash_flow_greater_than_net_income_report")
def cash_flow_greater_than_net_income_enrich_operation(stock):
    stock.update_report_in_metadata({
        constants.CASH_FLOWS: [stock.find_cash_flow(year) for year in stock.get_financial_year_of_results()],
        constants.INCOMES: [stock.get_net_income(year) for year in stock.get_financial_year_of_results()]
    })
