from screener.filters.factory import register_filter_operation, register_enrich_operation

WORKING_DAYS_IN_YEAR = 247  # holidays adjusted roughly number


@register_filter_operation("near_min_index_filter")
def minimum_index_filter(index, years, not_more_than_min_by_percentage):
    days = int(years * WORKING_DAYS_IN_YEAR)
    minimum_price = get_minimum_price(index, days)
    maximum_allowed_price = minimum_price * (1 + 0.01 * not_more_than_min_by_percentage)
    return index.get_current_value() <= maximum_allowed_price


def get_minimum_price(index, days):
    number_of_days_since_index_formed = index.number_of_days_since_index_formed()
    days_to_consider = min(days, number_of_days_since_index_formed)
    minimum_value = index.minimum_value_in_given_days(days_to_consider)
    return minimum_value


@register_enrich_operation("minimum_index_value_report")
def minimum_price_enrich_operation(index, in_years):
    minimum_value_in_years = get_minimum_price(index, int(in_years * WORKING_DAYS_IN_YEAR))
    more_than_minimum_price = ((index.get_current_value() - minimum_value_in_years) * 100) / minimum_value_in_years
    index.update_report_in_metadata({
        "minimum_value": minimum_value_in_years,
        "current_value": index.get_current_value(),
        "more_than_minimum_value": more_than_minimum_price
    })
