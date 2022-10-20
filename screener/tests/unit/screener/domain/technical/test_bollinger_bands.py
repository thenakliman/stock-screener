from unittest import TestCase

from screener.domain.technical.bollinger_bands import BollingerBand


class TestBollingerBand(TestCase):
    def setUp(self):
        self.bollinger_band = BollingerBand(10, 15, "12")

    def test_get_upper_band(self):
        self.assertEqual(15, self.bollinger_band.get_upper_band())

    def test_get_lower_band(self):
        self.assertEqual(10, self.bollinger_band.get_lower_band())

    def test_get_date(self):
        self.assertEqual("12", self.bollinger_band.get_date())
