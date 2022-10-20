from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("debt")
@register_enrich_operation("debt")
def debt_filter_operation(stock, debt_amount):
    return stock.get_long_term_debts(stock.find_financial_year_of_latest_results()) <= debt_amount


@register_filter_operation("debt_to_equity")
@register_enrich_operation("debt_to_equity")
def debt_to_equity_filter_operation(stock, less_than_equal_to: float) -> bool:
    return stock.get_debt_to_equity_ratio(stock.find_financial_year_of_latest_results()) <= less_than_equal_to


@register_filter_operation("debt_to_equity_less_than_industry")
@register_enrich_operation("debt_to_equity_less_than_industry")
def debt_to_equity_less_than_industry_filter_operation(stock, less_than_industry_by_percentage: float) -> bool:
    return stock.debt_to_equity_is_less_than_industry(less_than_industry_by_percentage)


@register_enrich_operation("debt_to_equity_report")
def debt_to_equity_enrich_operation(stock) -> None:
    stock.update_report_in_metadata({
        "debt_to_equity": [stock.get_debt_to_equity_ratio(year) for year in stock.get_financial_year_of_results()],
        "latest_debt_to_equity": stock.get_debt_to_equity_ratio(stock.find_financial_year_of_latest_results()),
        "industry_debt_to_equity": stock.get_sector_debt_to_equity()
    })


@register_enrich_operation("debt_report")
def debt_enrich_operation(stock):
    stock.update_report_in_metadata({
        "debt": [stock.get_debt(year) for year in stock.get_financial_year_of_results()]
    })
