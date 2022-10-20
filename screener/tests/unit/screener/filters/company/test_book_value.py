from unittest import TestCase, mock

from screener.filters.stock.book_value import (
    book_value_enrich_operation,
    book_value_filter_operation,
    price_to_book_less_than_industry_filter_operation
)


class TestBookValue(TestCase):
    def test_book_value_enrich_operation__add_price_to_book_value(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_price_to_book_value=lambda: 10,
                          get_industry_price_to_book_value=lambda: 2,
                          update_report_in_metadata=update_report_in_metadata)

        book_value_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({"price_to_book": 10, "industry_price_to_book_value": 2})

    def test_book_value_filter_operation__return_false__when_book_value_is_greater_than_given(self):
        stock = mock.Mock(get_price_to_book_value=lambda: 10)

        self.assertFalse(book_value_filter_operation(stock, 9))

    def test_price_to_book_less_than_industry_filter_operation__return_false(self):
        stock = mock.Mock(price_to_book_less_than_industry=lambda x: False)

        self.assertFalse(price_to_book_less_than_industry_filter_operation(stock, 9))

    def test_price_to_book_less_than_industry_filter_operation__return_true(self):
        stock = mock.Mock(price_to_book_less_than_industry=lambda x: True)

        self.assertTrue(price_to_book_less_than_industry_filter_operation(stock, 9))

    def test_book_value_filter_operation__return_true__when_book_value_is_less_than_given(self):
        stock = mock.Mock(get_price_to_book_value=lambda: 8)

        self.assertTrue(book_value_filter_operation(stock, 9))

    def test_book_value_filter_operation__return_false__when_book_value_is_equal_to_given(self):
        stock = mock.Mock(get_price_to_book_value=lambda: 9)

        self.assertFalse(book_value_filter_operation(stock, 9))
