from unittest import TestCase, mock

from screener.filters.stock.near_max_filter import maximum_price_filter_operation, \
    maximum_price_enrich_operation


class MaximumPriceTest(TestCase):
    def test_maximum_price_filter_operation__true__when_price_is_less_than_maximum_percentage(self):
        maximum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 89,
                          number_of_days_stock_in_market=lambda: 19,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        self.assertTrue(maximum_price_filter_operation(stock, 1.2, 10))
        maximum_price_in_given_days.assert_called_with(19)

    def test_maximum_price_filter_operation__false__when_price_is_greater_than_maximum_percentage(self):
        maximum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 91,
                          number_of_days_stock_in_market=lambda: 19,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        self.assertFalse(maximum_price_filter_operation(stock, 1.2, 10))
        maximum_price_in_given_days.assert_called_with(19)

    def test_maximum_price_filter_operation__true__when_price_is_equal_to_maximum_percentage(self):
        maximum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 90,
                          number_of_days_stock_in_market=lambda: 19,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        self.assertTrue(maximum_price_filter_operation(stock, 1.2, 10))
        maximum_price_in_given_days.assert_called_with(19)

    def test_maximum_price_filter__when_stock_in_market_is_more_than_given_criteria_use_criteria(self):
        maximum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 90,
                          number_of_days_stock_in_market=lambda: 500,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        self.assertTrue(maximum_price_filter_operation(stock, 1, 10))
        maximum_price_in_given_days.assert_called_with(247)

    def test_maximum_price_filter__when_stock_in_market_is_less_than_given_criteria_use_market_days(self):
        maximum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 90,
                          number_of_days_stock_in_market=lambda: 100,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        self.assertTrue(maximum_price_filter_operation(stock, 1.2, 10))
        maximum_price_in_given_days.assert_called_with(100)

    @staticmethod
    def test_maximum_price_enrich_operation__when_price_is_less_than_maximum_percentage():
        maximum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: 90,
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        maximum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "maximum_price": 100,
            "current_price": 90,
            "less_than_maximum_price": 10,
        })

    @staticmethod
    def test_maximum_price_enrich_operation__when_price_is_equal_to_maximum_percentage():
        maximum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: 100,
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          maximum_price_in_given_days=maximum_price_in_given_days)

        maximum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "maximum_price": 100,
            "current_price": 100,
            "less_than_maximum_price": 0,
        })
