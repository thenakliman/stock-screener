from unittest import TestCase, mock

from screener.filters.stock.graham_number import graham_number_filter_operation, graham_number_enrich_operation


class GrahamNumberTest(TestCase):
    def test_graham_number_filter_operation__true__when_price_is_less_than_graham_number(self):
        stock = mock.Mock(get_graham_number=lambda: 29,
                          get_current_price=lambda: 10)

        self.assertTrue(graham_number_filter_operation(stock))

    def test_graham_number_filter_operation__true__when_price_is_equal_than_graham_number(self):
        stock = mock.Mock(get_graham_number=lambda: 10,
                          get_current_price=lambda: 10)

        self.assertTrue(graham_number_filter_operation(stock))

    def test_graham_number_filter_operation__false__when_price_is_greater_than_graham_number(self):
        stock = mock.Mock(get_graham_number=lambda: 29,
                          get_current_price=lambda: 30)

        self.assertFalse(graham_number_filter_operation(stock))

    @staticmethod
    def test_graham_number_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_graham_number=lambda: 39)

        graham_number_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "graham_number": 39
        })
