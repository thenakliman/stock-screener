import unittest
from unittest import mock

from screener.filters.stock.net_income import (
    net_income_filter_operation,
    positive_net_income_filter_operation,
    net_income_enrich_operation, increasing_net_income)


class NetIncomeTest(unittest.TestCase):
    def test_net_income_filter_operation_return_true_when_more_than_required(self):
        mocked_get_net_income = mock.Mock(return_value=1900)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertTrue(net_income_filter_operation(stock, 1899))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    def test_net_income_filter_operation_return_false_when_less_than_required(self):
        mocked_get_net_income = mock.Mock(return_value=1900)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertFalse(net_income_filter_operation(stock, 1901))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    def test_net_income_filter_operation_return_true_when_less_than_required(self):
        mocked_get_net_income = mock.Mock(return_value=1900)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertTrue(net_income_filter_operation(stock, 1900))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    def test_increasing_net_income__true__when_more_than_required(self):
        mocked_net_income_increasing = mock.Mock(return_value=True)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          net_income_increasing=mocked_net_income_increasing)

        self.assertTrue(increasing_net_income(stock, 1899, 0.1))

        mocked_net_income_increasing.assert_called_with(19, 1899, 0.1)
        mocked_get_financial_year.assert_called_with()

    def test_increasing_net_income__false__when_less_than_required(self):
        mocked_net_income_increasing = mock.Mock(return_value=False)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          net_income_increasing=mocked_net_income_increasing)

        self.assertFalse(increasing_net_income(stock, 1901, 0.1))

        mocked_net_income_increasing.assert_called_with(19, 1901, 0.1)
        mocked_get_financial_year.assert_called_with()

    def test_increasing_net_income__true__when_less_than_required(self):
        mocked_net_income_increasing = mock.Mock(return_value=True)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          net_income_increasing=mocked_net_income_increasing)

        self.assertTrue(increasing_net_income(stock, 1900, 0.1))

        mocked_net_income_increasing.assert_called_with(19, 1900, 0.1)
        mocked_get_financial_year.assert_called_with()

    def test_positive_net_income_filter_operation_return_true_when_positive(self):
        mocked_get_net_income = mock.Mock(return_value=1900)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertTrue(positive_net_income_filter_operation(stock))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    def test_positive_net_income_filter_operation_return_false_when_negative(self):
        mocked_get_net_income = mock.Mock(return_value=-198)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertFalse(positive_net_income_filter_operation(stock))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    def test_positive_net_income_filter_operation_return_false_when_equal_to_zero(self):
        mocked_get_net_income = mock.Mock(return_value=0)
        mocked_get_financial_year = mock.Mock(return_value=19)
        stock = mock.Mock(find_financial_year_of_latest_results=mocked_get_financial_year,
                          get_net_income=mocked_get_net_income)

        self.assertFalse(positive_net_income_filter_operation(stock))

        mocked_get_net_income.assert_called_with(19)
        mocked_get_financial_year.assert_called_with()

    @staticmethod
    def test_net_income_enrich_operation():
        def get_net_income(year):
            return year * 17

        mocked_get_financial_year_of_results = mock.Mock(return_value=[18, 19])
        mocked_update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_financial_year_of_results=mocked_get_financial_year_of_results,
                          get_net_income=get_net_income,
                          update_report_in_metadata=mocked_update_report_in_metadata)

        net_income_enrich_operation(stock)

        mocked_update_report_in_metadata.assert_called_with({"incomes": [306, 323]})
        mocked_get_financial_year_of_results.assert_called_with()
