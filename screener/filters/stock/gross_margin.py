from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("gross_margin")
@register_enrich_operation("gross_margin")
def gross_margin_filter_operation(stock):
    return stock.increasing_gross_margin(stock.find_financial_year_of_latest_results())


@register_filter_operation("gross_margin_is_greater_than_sector")
@register_enrich_operation("gross_margin_is_greater_than_sector")
def sector_gross_margin_filter_operation(stock):
    return stock.gross_margin_is_greater_than_sector(stock.find_financial_year_of_latest_results())


@register_enrich_operation("gross_margin_report")
def gross_margin_enrich_operation(stock):
    stock.update_report_in_metadata({
        "gross_margin": [stock.get_gross_margin(year) for year in stock.get_financial_year_of_results()]
    })
