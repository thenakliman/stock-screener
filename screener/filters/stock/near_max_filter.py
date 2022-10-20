from screener.filters.factory import register_enrich_operation, register_filter_operation

WORKING_DAYS_IN_YEAR = 247  # holidays adjusted


@register_filter_operation("maximum_price")
@register_enrich_operation("maximum_price")
def maximum_price_filter_operation(stock, years, less_than_maximum_value_in_percentage):
    days = int(years * WORKING_DAYS_IN_YEAR)

    maximum_price = get_maximum_price(stock, days)
    maximum_allowed_price = maximum_price * (1 - .01 * less_than_maximum_value_in_percentage)
    return stock.get_current_price() <= maximum_allowed_price


def get_maximum_price(stock, days):
    total_number_of_days_stock_in_market = stock.number_of_days_stock_in_market()
    days_to_consider = min(days, total_number_of_days_stock_in_market)
    return stock.maximum_price_in_given_days(days_to_consider)


@register_enrich_operation("maximum_price_report")
def maximum_price_enrich_operation(stock, in_years):
    maximum_price_in_years = get_maximum_price(stock, int(in_years * WORKING_DAYS_IN_YEAR))
    stock.update_report_in_metadata({
        "maximum_price": maximum_price_in_years,
        "current_price": stock.get_current_price(),
        "less_than_maximum_price": ((maximum_price_in_years - stock.get_current_price()) * 100) / maximum_price_in_years
    })
