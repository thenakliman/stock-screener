from unittest import TestCase, mock

from screener.filters.stock.market_capital import market_capital_filter_operation, \
    market_capital_enrich_operation


class MarketCapitalTest(TestCase):
    def test_market_capital_filter_operation__true__market_capital_is_greater_than_minimum_capital(self):
        stock = mock.Mock(get_market_capital=lambda: 100)

        self.assertTrue(market_capital_filter_operation(stock, 80))

    def test_market_capital_filter_operation__false__market_capital_is_less_than_minimum_capital(self):
        stock = mock.Mock(get_market_capital=lambda: 60)

        self.assertFalse(market_capital_filter_operation(stock, 80))

    def test_market_capital_filter_operation__true__market_capital_is_equal_to_minimum_capital(self):
        stock = mock.Mock(get_market_capital=lambda: 80)

        self.assertTrue(market_capital_filter_operation(stock, 80))

    @staticmethod
    def test_market_capital_enrich_operation():
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          get_market_capital=lambda: 100)

        market_capital_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "market_capital": 100
        })
