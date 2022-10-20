from screener.filters.factory import register_enrich_operation, register_filter_operation

WORKING_DAYS_IN_YEAR = 247  # holidays adjusted


@register_filter_operation("near_max_index_filter")
def maximum_value_filter_operation(index, years, less_than_maximum_value_in_percentage):
    days = int(years * WORKING_DAYS_IN_YEAR)

    maximum_value = get_maximum_value(index, days)
    maximum_allowed_value = maximum_value * (1 - .01 * less_than_maximum_value_in_percentage)
    return index.get_current_value() < maximum_allowed_value


def get_maximum_value(index, days):
    total_number_of_days_stock_in_market = index.number_of_days_since_index_formed()
    days_to_consider = min(days, total_number_of_days_stock_in_market)
    maximum_value = index.maximum_value_in_given_days(days_to_consider)
    return maximum_value


@register_enrich_operation("maximum_index_value_report")
def maximum_value_enrich_operation(index, in_years):
    maximum_value_in_years = get_maximum_value(index, int(in_years * WORKING_DAYS_IN_YEAR))
    index.update_report_in_metadata({
        "maximum_value": maximum_value_in_years,
        "current_value": index.get_current_value(),
        "less_than_maximum_value": ((maximum_value_in_years - index.get_current_value()) * 100) / maximum_value_in_years
    })
