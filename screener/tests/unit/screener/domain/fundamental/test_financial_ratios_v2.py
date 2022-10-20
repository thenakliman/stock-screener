import unittest

from screener.domain.fundamental.financial_ratio import FinancialRatio


class FinancialRatiosTest(unittest.TestCase):
    def setUp(self):
        self.financial_ratios = FinancialRatio(
            current_ratio=1.1,
            gross_margin=1200,
            asset_turnover_ratio=1.2,
            return_on_asset=3,
            financial_year=2022,
            date_created="12-01-2022",
            last_date_updated="12-02-2022"
        )

    def test_get_current_ratio(self):
        self.assertEqual(1.1, self.financial_ratios.get_current_ratio())

    def test_get_asset_turnover(self):
        self.assertEqual(1.2, self.financial_ratios.get_asset_turnover())

    def test_get_return_on_asset(self):
        self.assertEqual(3, self.financial_ratios.get_return_on_asset())

    def test_get_gross_margin(self):
        self.assertEqual(1200, self.financial_ratios.get_gross_margin())

    def test_get_financial_year(self):
        self.assertEqual(2022, self.financial_ratios.get_financial_year())

    def test_to_dict(self):
        self.assertDictEqual({
            "current_ratio": 1.1,
            "gross_margin": 1200,
            "asset_turnover_ratio": 1.2,
            "return_on_asset": 3,
            "financial_year": 2022,
            "date_created": "12-01-2022",
            "last_date_updated": "12-02-2022"
        }, self.financial_ratios.to_dict())
