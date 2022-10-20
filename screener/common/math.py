import traceback

from screener.common.constants import NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE
from screener.exceptions.not_found import DataNotFound


def average(operation, stocks):
    running_sum = 0
    valid_stocks_operation = 0
    for stock in stocks:
        try:
            running_sum += operation(stock)
        except DataNotFound:
            print("Failed to perform operation for average calculation", stock.get_isinid())
        except Exception:
            traceback.print_exc()
        else:
            valid_stocks_operation += 1

    return running_sum / (valid_stocks_operation or NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE)


def standard_deviation(day_values, operation):
    value_average = average(operation, day_values)
    running_sum_of_diff_with_mean = 0
    for day_value in day_values:
        running_sum_of_diff_with_mean += (operation(day_value) - value_average) ** 2

    return (running_sum_of_diff_with_mean / len(day_values)) ** 0.5


def _get_simple_average(objects, value_key):
    values = [object_[value_key] for object_ in objects]
    return sum(values) / len(values)


def get_simple_moving_averages(values, number_of_days=20, value_key="value"):
    minimum_number_of_days = min(len(values), number_of_days)
    simple_average = _get_simple_average(values[:number_of_days], value_key)
    simple_moving_average = [{"date": values[minimum_number_of_days - 1]["date"], "value": simple_average}]
    current_moving_average = simple_average
    for index, value in enumerate(values[number_of_days:], start=number_of_days):
        current_value_contribution = value[value_key] / number_of_days
        last_value_contribution = values[index - number_of_days][value_key] / number_of_days
        current_moving_average = current_moving_average + current_value_contribution - last_value_contribution
        simple_moving_average.append({"date": value["date"], "value": current_moving_average})

    return simple_moving_average


def _get_smoothing_factor(number_of_days, weightage_to_current_value=2):
    return weightage_to_current_value / (number_of_days + 1)


def get_exponential_moving_averages(values, number_of_days=20, value_key="value"):
    simple_average = _get_simple_average(values[:number_of_days], value_key)
    minimum_number_of_days = min(len(values), number_of_days)
    exponential_moving_average = [{
        "date": values[minimum_number_of_days - 1]["date"],
        "value": simple_average
    }]
    smoothing_factor = _get_smoothing_factor(number_of_days)
    exponential_average = simple_average
    for index, value in enumerate(values[number_of_days:], start=number_of_days + 1):
        current_value_contribution = value[value_key] * smoothing_factor
        exponential_average = current_value_contribution + exponential_average * (1 - smoothing_factor)
        exponential_moving_average.append({
            "date": value["date"],
            "value": exponential_average
        })

    return exponential_moving_average
