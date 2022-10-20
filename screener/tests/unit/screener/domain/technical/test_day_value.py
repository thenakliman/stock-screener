from unittest import TestCase

from screener.domain.technical.day_value import DayValue


class TestDayValue(TestCase):
    def setUp(self):
        self.day_value = DayValue("date", 10, 10, 2, 15, 100)

    def test_get_low(self):
        self.assertEqual(2, self.day_value.get_low())

    def test_get_high(self):
        self.assertEqual(15, self.day_value.get_high())

    def test_get_value(self):
        self.assertEqual(10, self.day_value.get_value())

    def test_get_typical_price(self):
        self.assertEqual(9, self.day_value.get_typical_value())

    def test_get_date(self):
        self.assertEqual("date", self.day_value.get_date())

    def test_gt_return_true(self):
        self.assertTrue(self.day_value > DayValue("data", 9, 9, 4, 13, 100))

    def test_gt_return_false(self):
        self.assertFalse(self.day_value > DayValue("data", 11, 11, 4, 13, 100))

    def test_lt_return_true(self):
        self.assertTrue(self.day_value < DayValue("data", 11, 11, 4, 13, 100))

    def test_lt_return_false(self):
        self.assertFalse(self.day_value < DayValue("data", 9, 9, 4, 13, 100))

    def test_get_volume_return_volume(self):
        self.assertEqual(100, DayValue("data", 9, 9, 4, 13, 100).get_volume())

    def test_get_raw_money_flow_return_volume(self):
        self.assertEqual(900, DayValue("data", 9, 9, 5, 13, 100).get_raw_money_flow())

    def test_to_dict(self):
        self.assertDictEqual({
            "date": "data",
            "value": 9,
            "open": 9,
            "low": 5,
            "high": 13,
            "volume": 100
        }, DayValue("data", 9, 9, 5, 13, 100).to_dict())
