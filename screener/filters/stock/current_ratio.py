from screener.filters.factory import register_enrich_operation, register_filter_operation


@register_filter_operation("current_ratio")
@register_enrich_operation("current_ratio")
def current_ratio_filter_operation(stock):
    return stock.increasing_current_ratio(stock.find_financial_year_of_latest_results())


@register_filter_operation("current_ratio_is_greater_than_sector")
@register_enrich_operation("current_ratio_is_greater_than_sector")
def sector_current_ratio_filter_operation(stock):
    return stock.current_ratio_is_greater_than_sector(stock.find_financial_year_of_latest_results())


@register_enrich_operation("current_ratio_report")
def current_ratio_enrich_operation(stock):
    stock.update_report_in_metadata({
        "current_ratio": [stock.get_current_ratio(year) for year in stock.get_financial_year_of_results()]
    })
