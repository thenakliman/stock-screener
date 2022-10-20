from unittest import TestCase

from screener.domain.technical.rsi import RSI


class TestRSI(TestCase):
    def setUp(self):
        self.rsi = RSI("date", 12)

    def test_match_date(self):
        self.assertEqual("date", self.rsi.get_date())

    def test_match_value(self):
        self.assertEqual(12, self.rsi.get_value())
