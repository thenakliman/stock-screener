from screener.filters.factory import register_filter_operation, register_enrich_operation

WORKING_DAYS_IN_YEAR = 247  # holidays adjusted


@register_filter_operation("minimum_price")
@register_enrich_operation("minimum_price")
def minimum_price_filter_operation(stock, years, not_more_than_min_by_percentage):
    days = int(years * WORKING_DAYS_IN_YEAR)
    minimum_price = get_minimum_price(stock, days)
    maximum_allowed_price = minimum_price * (1 + 0.01 * not_more_than_min_by_percentage)
    return stock.get_current_price() <= maximum_allowed_price


def get_minimum_price(stock, days: int) -> float:
    number_of_days_stock_in_market = stock.number_of_days_stock_in_market()
    days_to_consider = min(days, number_of_days_stock_in_market)
    return stock.minimum_price_in_given_days(days_to_consider)


@register_enrich_operation("minimum_price_report")
def minimum_price_enrich_operation(stock, in_years):
    minimum_price_in_years = get_minimum_price(stock, int(in_years * WORKING_DAYS_IN_YEAR))
    more_than_minimum_price = ((float(
        stock.get_current_price()) - minimum_price_in_years) * 100) / minimum_price_in_years
    stock.update_report_in_metadata({
        "minimum_price": minimum_price_in_years,
        "current_price": stock.get_current_price(),
        "more_than_minimum_price": more_than_minimum_price
    })
