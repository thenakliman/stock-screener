from functools import reduce

from screener.common.constants import NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE


class MoneyFlowIndex:
    def __init__(self, date, value):
        self._date = date
        self._value = value

    def get_value(self):
        return self._value

    def get_date(self):
        return self._date


def _get_profit(day_values):
    return reduce(
        lambda accumulator, index_value_pair: accumulator + (
            index_value_pair[1].get_raw_money_flow()
            if index_value_pair[1].get_raw_money_flow() > day_values[
                index_value_pair[0]].get_raw_money_flow() else 0),
        enumerate(day_values[1:]),
        0)


def _get_loss(day_values):
    return reduce(
        lambda accumulator, index_value_pair: accumulator + (
            index_value_pair[1].get_raw_money_flow()
            if index_value_pair[1].get_raw_money_flow() < day_values[
                index_value_pair[0]].get_raw_money_flow() else 0),
        enumerate(day_values[1:]),
        0)


def get_money_flow_index(time_series, days=14):
    profits = _get_profit(time_series[:days])
    losses = _get_loss(time_series[:days]) + NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE
    money_flow_indexes = []
    for index, day_value in enumerate(time_series[days:]):
        if day_value.get_raw_money_flow() > time_series[index].get_raw_money_flow():
            profits = profits + day_value.get_raw_money_flow()
        else:
            losses = losses + day_value.get_raw_money_flow()

        if index > 0:
            if time_series[index].get_raw_money_flow() < time_series[index - 1].get_raw_money_flow():
                losses -= time_series[index].get_raw_money_flow()
            elif time_series[index].get_raw_money_flow() > time_series[index - 1].get_raw_money_flow():
                profits -= time_series[index].get_raw_money_flow()

        money_flow_index = calculate_money_flow_index(profits, losses)
        money_flow_indexes.append(MoneyFlowIndex(day_value.get_date(), money_flow_index))

    return money_flow_indexes


def calculate_money_flow_index(profits, losses):
    return 100 - (100 / (1 + profits / losses))
