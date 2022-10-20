from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("market_capital")
@register_enrich_operation("market_capital")
def market_capital_filter_operation(stock, minimum_market_capital):
    return stock.get_market_capital() >= minimum_market_capital


@register_enrich_operation("market_capital_report")
def market_capital_enrich_operation(stock):
    stock.update_report_in_metadata({
        "market_capital": stock.get_market_capital()
    })
