import unittest
from unittest import mock

from screener.domain.fundamental.financial_ratios import FinancialRatioV2
from screener.exceptions.not_found import FinancialRatioNotFound


class FinancialRatiosTest(unittest.TestCase):
    def setUp(self):
        self.financial_ratios = FinancialRatioV2([
            mock.Mock(get_financial_year=lambda: 2022,
                      get_current_ratio=lambda: 1.4,
                      get_asset_turnover=lambda: 3.4,
                      get_gross_margin=lambda: 1000,
                      get_return_on_asset=lambda: 1.3,
                      to_dict=lambda: {"a": 3}),
            mock.Mock(get_financial_year=lambda: 2021,
                      get_current_ratio=lambda: 1.4,
                      get_asset_turnover=lambda: 2.3,
                      get_gross_margin=lambda: 1200,
                      to_dict=lambda: {"a": 2}),
            mock.Mock(get_financial_year=lambda: 2020,
                      get_current_ratio=lambda: 1.5,
                      get_asset_turnover=lambda: 2.3,
                      get_gross_margin=lambda: 1000,
                      to_dict=lambda: {"a": 1}),
            mock.Mock(get_financial_year=lambda: 2019,
                      get_current_ratio=lambda: 1.3,
                      get_asset_turnover=lambda: 4.3,
                      get_gross_margin=lambda: 1000,
                      to_dict=lambda: {"a": 10})
        ])

    def test_increasing_current_ratio__true__when_ratio_is_increasing(self):
        self.assertTrue(self.financial_ratios.increasing_current_ratio(2020))

    def test_increasing_current_ratio__false__when_ratio_are_equal(self):
        self.assertFalse(self.financial_ratios.increasing_current_ratio(2022))

    def test_increasing_current_ratio__false__when_ratio_are_decreasing(self):
        self.assertFalse(self.financial_ratios.increasing_current_ratio(2021))

    def test_get_current_ratio(self):
        self.assertEqual(1.4, self.financial_ratios.get_current_ratio(2021))

    def test_get_current_ratio__raise_exception__when_year_data_is_not_available(self):
        self.assertRaises(FinancialRatioNotFound, lambda: self.financial_ratios.get_current_ratio(2023))

    def test_increasing_gross_margin__true__when_ratio_is_increasing(self):
        self.assertTrue(self.financial_ratios.increasing_gross_margin(2021))

    def test_increasing_gross_margin__false__when_ratio_are_equal(self):
        self.assertFalse(self.financial_ratios.increasing_gross_margin(2020))

    def test_increasing_gross_margin__false__when_ratio_are_decreasing(self):
        self.assertFalse(self.financial_ratios.increasing_gross_margin(2022))

    def test_get_return_on_asset(self):
        self.assertEqual(1.3, self.financial_ratios.get_return_on_asset(2022))

    def test_increasing_asset_turnover_ratio__true__when_ratio_is_increasing(self):
        self.assertTrue(self.financial_ratios.increasing_asset_turnover_ratio(2022))

    def test_increasing_asset_turnover_ratio__false__when_ratio_are_equal(self):
        self.assertFalse(self.financial_ratios.increasing_asset_turnover_ratio(2021))

    def test_increasing_asset_turnover_ratio__false__when_ratio_are_decreasing(self):
        self.assertFalse(self.financial_ratios.increasing_asset_turnover_ratio(2020))

    def test_get_financial_year_of_results(self):
        self.assertTupleEqual(self.financial_ratios.get_financial_year_of_results(), (2022, 2021, 2020, 2019))
