from unittest import TestCase, mock

from screener.filters.stock.near_min_filter import (
    minimum_price_filter_operation,
    minimum_price_enrich_operation)


class NearMinFilterTest(TestCase):
    def test_minimum_price_filter_operation__true__when_price_is_more_than_minimum_percentage(self):
        minimum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 120,
                          number_of_days_stock_in_market=lambda: 19,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        self.assertTrue(minimum_price_filter_operation(stock, 1.2, 21))
        minimum_price_in_given_days.assert_called_with(19)

    def test_minimum_price_filter_operation__false__when_price_is_less_than_minimum_percentage(self):
        minimum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 111,
                          number_of_days_stock_in_market=lambda: 19,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        self.assertFalse(minimum_price_filter_operation(stock, 1.2, 10))
        minimum_price_in_given_days.assert_called_with(19)

    def test_minimum_price_filter_operation__true__when_price_is_equal_to_minimum_percentage(self):
        minimum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 110,
                          number_of_days_stock_in_market=lambda: 19,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        self.assertTrue(minimum_price_filter_operation(stock, 1.2, 10))
        minimum_price_in_given_days.assert_called_with(19)

    @staticmethod
    def test_minimum_price_filter__when_stock_in_market_is_more_than_given_criteria_use_criteria():
        minimum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 110,
                          number_of_days_stock_in_market=lambda: 500,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_filter_operation(stock, 1, 10)

        minimum_price_in_given_days.assert_called_with(247)

    @staticmethod
    def test_minimum_price_filter__when_stock_in_market_is_less_than_given_criteria_use_market_days():
        minimum_price_in_given_days = mock.Mock(return_value=100)
        stock = mock.Mock(get_current_price=lambda: 110,
                          number_of_days_stock_in_market=lambda: 100,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_filter_operation(stock, 1.2, 10)

        minimum_price_in_given_days.assert_called_with(100)

    @staticmethod
    def test_minimum_price_enrich_operation__when_price_is_less_than_minimum_percentage():
        minimum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: 112,
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "minimum_price": 100,
            "current_price": 112,
            "more_than_minimum_price": 12,
        })

    @staticmethod
    def test_minimum_price_enrich_operation__when_price_is_equal_to_minimum_price():
        minimum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: 100,
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "minimum_price": 100,
            "current_price": 100,
            "more_than_minimum_price": 0,
        })

    @staticmethod
    def test_minimum_price_enrich_operation__when_price_is_equal_to_maximum_price():
        minimum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: 340,
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "minimum_price": 100,
            "current_price": 340,
            "more_than_minimum_price": 240.0,
        })

    def test_minimum_price_enrich_operation__when_price_is_equal_to_maximum_price_string(self):
        minimum_price_in_given_days = mock.Mock(return_value=100)
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_current_price=lambda: "340",
                          number_of_days_stock_in_market=lambda: 100,
                          update_report_in_metadata=update_report_in_metadata,
                          minimum_price_in_given_days=minimum_price_in_given_days)

        minimum_price_enrich_operation(stock, 1.2)

        update_report_in_metadata.assert_called_with({
            "minimum_price": 100,
            "current_price": "340",
            "more_than_minimum_price": 240.0,
        })
