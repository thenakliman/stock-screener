from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("market_leader")
@register_enrich_operation("market_leader")
def market_leader_filter_operation(stock):
    return stock.market_leader()


@register_enrich_operation("market_leader_report")
def market_leader_enrich_operation(stock):
    stock.update_report_in_metadata({
        "market_leader": stock.market_leader()
    })
