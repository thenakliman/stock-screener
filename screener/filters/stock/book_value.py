from screener.filters.factory import register_filter_operation, register_enrich_operation


@register_filter_operation("price_to_book")
@register_enrich_operation("price_to_book")
def book_value_filter_operation(stock, price_to_book_ratio):
    return stock.get_price_to_book_value() < price_to_book_ratio


@register_filter_operation("price_to_book_less_than_industry")
@register_enrich_operation("price_to_book_less_than_industry")
def price_to_book_less_than_industry_filter_operation(stock, less_than_industry_by_percentage):
    return stock.price_to_book_less_than_industry(less_than_industry_by_percentage)


@register_enrich_operation("price_to_book_report")
def book_value_enrich_operation(stock):
    stock.update_report_in_metadata({
        "price_to_book": stock.get_price_to_book_value(),
        "industry_price_to_book_value": stock.get_industry_price_to_book_value()
    })
