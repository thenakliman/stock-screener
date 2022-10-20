from unittest import TestCase, mock

from screener.common import date
from screener.common.year import (
    is_latest_financial_year
)


class TestYear(TestCase):
    @mock.patch.object(date, "current_month", return_value=2)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__true__when_current_month_is_3_and_year_less_by_one(
            self, mocked_year, mocked_month):
        self.assertTrue(is_latest_financial_year(2021))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=2)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__false__when_current_month_is_3_and_year_is_equal(
            self, mocked_year, mocked_month):
        self.assertFalse(is_latest_financial_year(2022))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=4)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__true__when_current_month_is_4_and_year_less_by_one(
            self, mocked_year, mocked_month):
        self.assertTrue(is_latest_financial_year(2021))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=4)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__true__when_current_month_is_4_and_year_equal(self, mocked_year, mocked_month):
        self.assertTrue(is_latest_financial_year(2022))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=4)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__false__when_current_month_is_4_and_year_diff_2(self, mocked_year, mocked_month):
        self.assertFalse(is_latest_financial_year(2020))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=6)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__true__when_current_month_is_6_and_year_is_equal(self, mocked_year, mocked_month):
        self.assertTrue(is_latest_financial_year(2022))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=7)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year__true__when_current_month_is_7_and_year_is_equal(self, mocked_year, mocked_month):
        self.assertTrue(is_latest_financial_year(2022))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    @mock.patch.object(date, "current_month", return_value=7)
    @mock.patch.object(date, "current_year", return_value=2022)
    def test_is_latest_financial_year_false__when_current_month_is_7_and_year_is_equal(self, mocked_year, mocked_month):
        self.assertFalse(is_latest_financial_year(2021))
        mocked_month.assert_called_with()
        mocked_year.assert_called_with()

    def test_is_latest_financial_year_should_return_false_when_it_is_not_latest(self):
        self.assertFalse(is_latest_financial_year('20'))
