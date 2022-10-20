from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("graham_number")
@register_enrich_operation("graham_number")
def graham_number_filter_operation(stock):
    return stock.get_graham_number() >= stock.get_current_price()


@register_enrich_operation("graham_number_report")
def graham_number_enrich_operation(stock):
    stock.update_report_in_metadata({
        "graham_number": stock.get_graham_number()
    })
