import unittest

from screener.domain.technical.day_value import DayValue
from screener.domain.technical.rate_of_change import get_rate_of_change


class TestRateOfChange(unittest.TestCase):
    def test_rate_of_change__return_zero__when_there_is_no_change(self):
        time_series = [DayValue("1", 102, 102, 1, 2, 100),
                       DayValue("2", 102, 102, 1, 2, 100),
                       DayValue("3", 102, 102, 1, 2, 100),
                       DayValue("4", 102, 102, 1, 2, 100)]

        rate_of_changes = get_rate_of_change(time_series, 4)

        expected_values = [{
            "date": "1",
            "value": 0
        }, {
            "date": "2",
            "value": 0
        }, {
            "date": "3",
            "value": 0
        }, {
            "date": "4",
            "value": 0
        }]

        for index, roc in enumerate(rate_of_changes):
            self.assertEqual(expected_values[index]["date"], roc.get_date())
            self.assertEqual(expected_values[index]["value"], roc.get_value())

    def test_rate_of_change__return_roc__when_value_is_increasing(self):
        time_series = [DayValue("1", 102, 102, 1, 2, 100),
                       DayValue("2", 104, 104, 1, 2, 100),
                       DayValue("3", 106, 106, 1, 2, 100),
                       DayValue("4", 108, 108, 1, 2, 100)]

        rate_of_changes = get_rate_of_change(time_series, 2)

        expected_values = [{
            "date": "1",
            "value": 0
        }, {
            "date": "2",
            "value": 1.9607843137254901
        }, {
            "date": "3",
            "value": 3.9215686274509802
        }, {
            "date": "4",
            "value": 3.8461538461538463
        }]

        for index, roc in enumerate(rate_of_changes):
            self.assertEqual(roc.get_date(), expected_values[index]["date"])
            self.assertEqual(roc.get_value(), expected_values[index]["value"])

    def test_rate_of_change__return_roc__when_value_is_decreasing(self):
        time_series = [DayValue("1", 110, 110, 1, 2, 100),
                       DayValue("2", 108, 108, 1, 2, 100),
                       DayValue("3", 106, 106, 1, 2, 100),
                       DayValue("4", 104, 104, 1, 2, 100)]

        rate_of_changes = get_rate_of_change(time_series, 2)

        expected_values = [{
            "date": "1",
            "value": 0
        }, {
            "date": "2",
            "value": -1.8181818181818181
        }, {
            "date": "3",
            "value": -3.6363636363636362
        }, {
            "date": "4",
            "value": -3.7037037037037033
        }]

        for index, roc in enumerate(rate_of_changes):
            self.assertEqual(roc.get_date(), expected_values[index]["date"])
            self.assertEqual(roc.get_value(), expected_values[index]["value"])
