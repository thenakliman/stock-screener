from unittest import TestCase, mock

from screener.common.math import average, get_simple_moving_averages, get_exponential_moving_averages, \
    standard_deviation
from screener.domain.technical.day_value import DayValue
from screener.exceptions.not_found import DataNotFound


class Test(TestCase):
    def test_average_return_average_when_operation_is_successful(self):
        def operation(stock):
            return stock()

        average_value = average(operation,
                                [mock.Mock(return_value=1),
                                 mock.Mock(return_value=2),
                                 mock.Mock(return_value=3)])

        self.assertEqual(average_value, 2)

    def test_average_return_average_when_operation_fails(self):
        def operation(stock):
            return stock()

        average_value = average(operation,
                                [mock.Mock(return_value=1),
                                 mock.Mock(side_effect=ValueError),
                                 mock.Mock(return_value=3)])

        self.assertEqual(average_value, 2)

    def test_average_return_average_when_operation_fails_with_data_not_found(self):
        def operation(stock):
            return stock()

        average_value = average(operation,
                                [mock.Mock(return_value=1),
                                 mock.Mock(side_effect=DataNotFound),
                                 mock.Mock(side_effect=ValueError)])

        self.assertEqual(average_value, 1)

    def test_average_return_average_when_all_operation_fails(self):
        def operation(stock):
            return stock()

        average_value = average(operation,
                                [mock.Mock(side_effect=ValueError),
                                 mock.Mock(side_effect=ValueError),
                                 mock.Mock(side_effect=ValueError)])

        self.assertEqual(average_value, 0)

    def test_get_simple_moving_average_when_all_values_are_the_same(self):
        values = [{
            "date": "1",
            "value": 2
        }, {
            "date": "2",
            "value": 2
        }, {
            "date": "3",
            "value": 2
        }, {
            "date": "4",
            "value": 2
        }, {
            "date": "5",
            "value": 2
        }]

        simple_average = get_simple_moving_averages(values, 2)

        self.assertEqual([{'date': '2', 'value': 2.0},
                          {'date': '3', 'value': 2.0},
                          {'date': '4', 'value': 2.0},
                          {'date': '5', 'value': 2.0}],
                         simple_average)

    def test_get_simple_moving_average_when_values_are_different(self):
        values = [{
            "date": "1",
            "value": 4
        }, {
            "date": "2",
            "value": 2
        }, {
            "date": "3",
            "value": 10
        }, {
            "date": "4",
            "value": 4
        }, {
            "date": "5",
            "value": 5
        }]

        simple_average = get_simple_moving_averages(values, 2)

        self.assertEqual([{'date': '2', 'value': 3.0},
                          {'date': '3', 'value': 6.0},
                          {'date': '4', 'value': 7.0},
                          {'date': '5', 'value': 4.5}],
                         simple_average)

    def test_get_exponential_moving_averages_when_all_values_are_the_same(self):
        values = [{
            "date": "1",
            "value": 2.0
        }, {
            "date": "2",
            "value": 2.0
        }, {
            "date": "3",
            "value": 2.0
        }, {
            "date": "4",
            "value": 2.0
        }, {
            "date": "5",
            "value": 2.0
        }]

        exponential_average = get_exponential_moving_averages(values, 2)

        self.assertEqual([{'date': '2', 'value': 2.0},
                          {'date': '3', 'value': 2.0},
                          {'date': '4', 'value': 2.0},
                          {'date': '5', 'value': 2.0}],
                         exponential_average)

    def test_get_exponential_moving_averages_when_values_are_different(self):
        values = [{
            "date": "1",
            "value": 4
        }, {
            "date": "2",
            "value": 2
        }, {
            "date": "3",
            "value": 10
        }, {
            "date": "4",
            "value": 4
        }, {
            "date": "5",
            "value": 5
        }]

        simple_average = get_exponential_moving_averages(values, 2)

        self.assertEqual([{'date': '2', 'value': 3.0},
                          {'date': '3', 'value': 7.666666666666666},
                          {'date': '4', 'value': 5.222222222222222},
                          {'date': '5', 'value': 5.074074074074074}],
                         simple_average)

    def test_get_exponential_moving_averages_when_values_are_different_and_number_of_days_one(self):
        values = [{
            "date": "1",
            "value": 4
        }, {
            "date": "2",
            "value": 2
        }, {
            "date": "3",
            "value": 10
        }, {
            "date": "4",
            "value": 4
        }, {
            "date": "5",
            "value": 5
        }]

        exponential_average = get_exponential_moving_averages(values, 1)

        self.assertEqual([{'date': '1', 'value': 4.0},
                          {'date': '2', 'value': 2.0},
                          {'date': '3', 'value': 10.0},
                          {'date': '4', 'value': 4.0},
                          {'date': '5', 'value': 5.0}],
                         exponential_average)

    def test_standard_deviation_when_low_high_and_value_are_equal(self):
        values = [
            DayValue("1", 727.7, 727.7, 727.7, 727.7, 0),
            DayValue("2", 1086.5, 1086.5, 1086.5, 1086.5, 0),
            DayValue("3", 1091.0, 1091.0, 1091.0, 1091.0, 0),
            DayValue("4", 1361.3, 1361.3, 1361.3, 1361.3, 0),
            DayValue("5", 1490.5, 1490.5, 1490.5, 1490.5, 0),
            DayValue("6", 1956.1, 1956.1, 1956.1, 1956.1, 0)
        ]

        sd = standard_deviation(values, lambda day_value: day_value.get_typical_value())

        self.assertEqual(sd, 384.2844190469113)

    def test_standard_deviation_when_low_high_and_value_are_not_equal(self):
        values = [
            DayValue("1", 800, 800, 900, 100, 0),
            DayValue("2", 870, 870, 400, 140, 0),
            DayValue("3", 300, 300, 120, 90, 0),
            DayValue("4", 700, 700, 300, 290, 0),
            DayValue("5", 700, 700, 150, 50, 0)
        ]

        sd = standard_deviation(values, lambda day_value: day_value.get_typical_value())

        self.assertEqual(sd, 147.32277488562318)
