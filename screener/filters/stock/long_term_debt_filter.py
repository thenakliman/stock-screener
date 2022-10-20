from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("long_term_debt")
@register_enrich_operation("long_term_debt")
def long_term_debt_filter_operation(stock):
    return stock.decreasing_long_term_debt_ratio_by_year(stock.find_financial_year_of_latest_results())


@register_enrich_operation("long_term_debt_report")
def long_term_debt_enrich_operation(stock):
    stock.update_report_in_metadata({
        "long_term_debts": [stock.get_long_term_debts(year) for year in stock.get_financial_year_of_results()]
    })
