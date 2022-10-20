import unittest

from screener.domain.technical.day_value import DayValue
from screener.domain.technical.money_flow_index import get_money_flow_index


class TestMoneyFlowIndex(unittest.TestCase):
    def test_money_flow_index__return_zero__when_values_are_decreasing(self):
        time_series = [DayValue("1", 110, 110, 4, 2, 100),
                       DayValue("2", 108, 108, 4, 2, 100),
                       DayValue("3", 106, 106, 4, 2, 100),
                       DayValue("4", 104, 104, 4, 2, 100),
                       DayValue("5", 102, 102, 4, 2, 100),
                       DayValue("6", 100, 100, 4, 2, 100)]

        money_flow_indexes = get_money_flow_index(time_series, 3)

        expected_values = [{
            "value": 0,
            "date": "4"
        }, {
            "value": 0,
            "date": "5"
        }, {
            "value": 0,
            "date": "6"
        }]

        for index, money_flow in enumerate(money_flow_indexes):
            self.assertEqual(money_flow.get_value(), expected_values[index]["value"])
            self.assertEqual(money_flow.get_date(), expected_values[index]["date"])

    def test_money_flow_index__return_zero__when_volume_is_zero(self):
        time_series = [DayValue("1", 110, 110, 4, 2, 0),
                       DayValue("2", 108, 108, 4, 2, 0),
                       DayValue("3", 109, 109, 4, 2, 0),
                       DayValue("4", 104, 104, 4, 2, 0),
                       DayValue("5", 112, 112, 4, 2, 0),
                       DayValue("6", 100, 100, 4, 2, 0)]

        money_flow_indexes = get_money_flow_index(time_series, 3)

        expected_values = [{
            "value": 0,
            "date": "4"
        }, {
            "value": 0,
            "date": "5"
        }, {
            "value": 0,
            "date": "6"
        }]

        for index, money_flow in enumerate(money_flow_indexes):
            self.assertEqual(money_flow.get_value(), expected_values[index]["value"])
            self.assertEqual(money_flow.get_date(), expected_values[index]["date"])

    def test_money_flow_index__return_closer_to_100__when_values_are_increasing(self):
        time_series = [DayValue("1", 110, 110, 4, 2, 100),
                       DayValue("2", 112, 112, 4, 2, 100),
                       DayValue("3", 114, 114, 4, 2, 100),
                       DayValue("4", 116, 116, 4, 2, 100),
                       DayValue("5", 118, 118, 4, 2, 100),
                       DayValue("6", 120, 120, 4, 2, 100)]

        money_flow_indexes = get_money_flow_index(time_series, 3)

        expected_values = [{
            "value": 99.99991666673611,
            "date": "4"
        }, {
            "value": 99.99991803285407,
            "date": "5"
        }, {
            "value": 99.99991935490375,
            "date": "6"
        }]

        for index, money_flow in enumerate(money_flow_indexes):
            self.assertEqual(expected_values[index]["value"], money_flow.get_value(), )
            self.assertEqual(expected_values[index]["date"], money_flow.get_date())

    def test_money_flow_index__return_money_flow_index(self):
        time_series = [DayValue("1", 110, 110, 4, 2, 100),
                       DayValue("2", 100, 100, 4, 2, 100),
                       DayValue("3", 102, 102, 4, 2, 100),
                       DayValue("4", 94, 94, 4, 2, 100),
                       DayValue("5", 104, 104, 4, 2, 100),
                       DayValue("6", 101, 101, 4, 2, 100)]

        money_flow_indexes = get_money_flow_index(time_series, 3)

        expected_values = [{
            "value": 34.394871597256426,
            "date": "4"
        }, {
            "value": 68.55339444648322,
            "date": "5"
        }, {
            "value": 34.700282618029064,
            "date": "6"
        }]

        for index, money_flow in enumerate(money_flow_indexes):
            self.assertEqual(money_flow.get_value(), expected_values[index]["value"])
            self.assertEqual(money_flow.get_date(), expected_values[index]["date"])
