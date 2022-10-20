from typing import List, Optional

from screener.common import math
from screener.common.constants import NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE
from screener.domain.technical.average import Average
from screener.domain.technical.bollinger_bands import BollingerBand
from screener.domain.technical.day_value import DayValue
from screener.domain.technical.rsi import RSI
from screener.domain.technical.stochastic_oscillator import StochasticOscillator
from screener.exceptions.not_found import (
    HistoricalPricesIsNotAvailable
)


class HistoricalValues:
    def __init__(self, day_values=None):
        self._day_values = day_values or []

    @staticmethod
    def _get_simple_average_of_given_data(item_values):
        values = [day_value.get_value() for day_value in item_values]
        return float(sum(values)) / len(values)

    def _get_simple_average(self, simple_average_of_days=None):
        simple_average_of_days = simple_average_of_days or len(self._day_values)
        values_of_days = [day_value.get_value() for day_value in self._day_values[:simple_average_of_days]]
        return sum(values_of_days) / len(values_of_days)

    def get_simple_moving_averages(self, number_of_days):
        minimum_number_of_days = min(len(self._day_values), number_of_days)
        simple_average = self._get_simple_average(number_of_days)
        day_value_on_first_date = Average(self._day_values[minimum_number_of_days - 1].get_date(), simple_average)
        simple_moving_average = [day_value_on_first_date]
        current_moving_average = simple_average
        for index, day_value in enumerate(self._day_values[number_of_days:], start=number_of_days):
            current_value_contribution = day_value.get_value() / number_of_days
            last_value_contribution = self._day_values[index - number_of_days].get_value() / number_of_days
            current_moving_average = current_moving_average + current_value_contribution - last_value_contribution
            simple_moving_average.append(Average(day_value.get_date(), current_moving_average))

        return simple_moving_average

    @staticmethod
    def _get_smoothing_factor(number_of_days, weightage_to_current_value=2):
        return weightage_to_current_value / (number_of_days + 1)

    def get_exponential_moving_averages(self, number_of_days=20):
        simple_average = self._get_simple_average(number_of_days)
        minimum_number_of_days = min(len(self._day_values), number_of_days)
        day_value_on_first_date = Average(self._day_values[minimum_number_of_days - 1].get_date(), simple_average)
        exponential_moving_average = [day_value_on_first_date]
        smoothing_factor = self._get_smoothing_factor(number_of_days)
        exponential_average = simple_average

        for index, day_values in enumerate(self._day_values[number_of_days:], start=number_of_days + 1):
            current_value_contribution = day_values.get_value() * smoothing_factor
            exponential_average = current_value_contribution + exponential_average * (1 - smoothing_factor)
            exponential_moving_average.append(Average(day_values.get_date(), exponential_average))

        return exponential_moving_average

    def golden_cross(self, long_term_in_days=200, short_term_in_days=15):
        long_term_moving_average_till_today = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - long_term_in_days:])
        short_term_moving_till_today = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - short_term_in_days:])

        long_term_moving_average_till_last_day = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - long_term_in_days - 1:][:-1])
        short_term_moving_till_last_day = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - short_term_in_days - 1:][:-1])

        return (long_term_moving_average_till_today <= short_term_moving_till_today) and \
               (long_term_moving_average_till_last_day > short_term_moving_till_last_day)

    def death_cross(self, long_term_in_days=200, short_term_in_days=15):
        long_term_moving_average_till_today = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - long_term_in_days:])
        short_term_moving_till_today = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - short_term_in_days:])
        long_term_moving_average_till_last_day = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - long_term_in_days - 1:][:-1])
        short_term_moving_till_last_day = self._get_simple_average_of_given_data(
            self._day_values[len(self._day_values) - short_term_in_days - 1:][:-1])
        return (long_term_moving_average_till_today >= short_term_moving_till_today) and \
               (long_term_moving_average_till_last_day < short_term_moving_till_last_day)

    def get_bollinger_band(self, days=20, number_of_sd=1):
        moving_average = math.average(lambda day_value: day_value.get_typical_value(),
                                      self._day_values[:days])
        bollinger_bands = []
        for index in range(days - 1, len(self._day_values)):
            sd = math.standard_deviation(self._day_values[index - days + 1: index + 1],
                                         lambda day_value: day_value.get_typical_value())
            bollinger_bands.append(
                BollingerBand(moving_average - number_of_sd * sd,
                              moving_average + number_of_sd * sd,
                              self._day_values[index].get_date())
            )

            if index == len(self._day_values) - 1:
                break

            moving_average = (moving_average
                              + (self._day_values[index + 1].get_typical_value() / days)
                              - (self._day_values[index - days + 1].get_typical_value()) / days)

        return bollinger_bands

    @staticmethod
    def _get_percentage(current_value, previous_value):
        if current_value > previous_value:
            return ((current_value - previous_value) / previous_value) * 100

        return ((previous_value - current_value) / previous_value) * 100

    @staticmethod
    def _get_rsi(gains_average, losses_average):
        losses_average += NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE
        return 100 - (100 / (1 + (gains_average / losses_average)))

    def _get_initial_gains_percentage(self, days):
        gains = 0
        for index in range(1, days):
            if self.in_profit(self._day_values[index].get_value(), self._day_values[index - 1].get_value()):
                gains += self._get_percentage(
                    self._day_values[index].get_value(),
                    self._day_values[index - 1].get_value()
                )

        return gains

    def _get_initial_loss_percentage(self, days):
        losses = 0
        for index in range(1, days):
            if self.in_loss(self._day_values[index].get_value(), self._day_values[index - 1].get_value()):
                losses += self._get_percentage(
                    self._day_values[index].get_value(),
                    self._day_values[index - 1].get_value()
                )

        return losses

    @staticmethod
    def in_loss(current_value, previous_value):
        return current_value < previous_value

    @staticmethod
    def in_profit(current_value, previous_value):
        return current_value > previous_value

    def get_relative_strength_index(self, days=14):
        gains = self._get_initial_gains_percentage(days)
        losses = self._get_initial_loss_percentage(days)

        rsis = [RSI(self._day_values[days - 1].get_date(), self._get_rsi(gains, losses))]
        for index in range(days, days + len(self._day_values[days:])):
            if self.in_profit(self._day_values[index], self._day_values[index - 1]):
                gains = gains * (days - 1) + self._get_percentage(self._day_values[index].get_value(),
                                                                  self._day_values[index - 1].get_value())
            elif self.in_loss(self._day_values[index], self._day_values[index - 1]):
                losses = losses * (days - 1) + self._get_percentage(self._day_values[index].get_value(),
                                                                    self._day_values[index - 1].get_value())

            rsi = self._get_rsi(gains, losses)
            rsis.append(RSI(self._day_values[index].get_date(), rsi))

        return rsis

    def _get_slow_stochastic_oscillator_for_a_day(self, index, days):
        low = 99999999
        high = 0
        for day_value in self._day_values[index - days + 1: index + 1]:
            if day_value.get_value() < low:
                low = day_value.get_value()
            if day_value.get_value() > high:
                high = day_value.get_value()

        return ((self._day_values[index].get_value() - low)
                / (high - low + NEGLIGIBLE_VALUE_TO_AVOID_DIVIDE_BY_ZERO_VALUE)) * 100

    def get_stochastic_oscillator(self, days, moving_average_for_fast_oscillator=3):
        fast_oscillator = 0
        stochastic_oscillators = []

        for index in range(days - 1, len(self._day_values)):
            slow_stochastic_oscillator = self._get_slow_stochastic_oscillator_for_a_day(index, days)

            contribution_by_current_value = self._stochastic_oscillator_contribution(
                slow_stochastic_oscillator,
                moving_average_for_fast_oscillator)

            contribution_by_value_moving_out_of_window = self._get_slow_stochastic_value_before_days(
                stochastic_oscillators,
                days,
                moving_average_for_fast_oscillator,
                index)

            fast_oscillator = (
                    fast_oscillator
                    + contribution_by_current_value
                    - contribution_by_value_moving_out_of_window)

            stochastic_oscillators.append(StochasticOscillator(
                self._day_values[index].get_date(),
                slow_stochastic_oscillator,
                fast_oscillator))

        return stochastic_oscillators

    @staticmethod
    def _stochastic_oscillator_contribution(slow_stochastic_oscillator, moving_average_for_fast_oscillator):
        return slow_stochastic_oscillator / moving_average_for_fast_oscillator

    @staticmethod
    def _get_slow_stochastic_value_before_days(stochastic_oscillators, days, moving_average_for_fast_oscillator, index):
        value_moving_out_of_window = 0
        if len(stochastic_oscillators) >= days:
            value_moving_out_of_window = stochastic_oscillators[-days].get_slow_oscillator()

        if index >= (moving_average_for_fast_oscillator + days - 1):
            return value_moving_out_of_window / moving_average_for_fast_oscillator

        return value_moving_out_of_window

    def to_dict(self) -> List[dict]:
        return [day_value.to_dict() for day_value in self._day_values]

    def get_date_of_latest_available_price(self) -> str:
        if len(self._day_values) == 0:
            return "01-01-1990"

        return self._day_values[-1].get_date()

    def get_current_price(self) -> Optional[str]:
        if len(self._day_values) == 0:
            return None

        return self._day_values[-1].get_value()

    def number_of_days_stock_in_market(self) -> int:
        return len(self._day_values)

    def minimum_price_in_given_days(self, days: int) -> float:
        number_of_days_stock_available_in_public = self.number_of_days_stock_in_market()
        index = number_of_days_stock_available_in_public - min(number_of_days_stock_available_in_public, days)
        minimum_price = float(self._day_values[-1].get_value())
        for day_value in self._day_values[index:]:
            minimum_price = min(minimum_price, float(day_value.get_value()))

        return minimum_price

    def maximum_price_in_given_days(self, days: int) -> float:
        number_of_days_stock_available_in_public = self.number_of_days_stock_in_market()
        index = number_of_days_stock_available_in_public - min(days, number_of_days_stock_available_in_public)
        maximum_price = float(self._day_values[-1].get_value())
        for day_value in self._day_values[index:]:
            maximum_price = max(maximum_price, float(day_value.get_value()))

        return maximum_price

    def add_latest_price(self, prices: List[DayValue]) -> None:
        self._day_values = self._day_values + prices

    def get_latest_price(self) -> DayValue:
        if len(self._day_values) == 0:
            raise HistoricalPricesIsNotAvailable()

        return self._day_values[-1]
