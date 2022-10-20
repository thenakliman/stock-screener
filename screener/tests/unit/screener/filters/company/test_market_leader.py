from unittest import TestCase, mock

from screener.filters.stock.market_leader import market_leader_filter_operation, market_leader_enrich_operation


class MarketLeaderTest(TestCase):
    def test_market_leader_filter_operation__true__stock_is_market_leader(self):
        stock = mock.Mock(market_leader=lambda: True)

        self.assertTrue(market_leader_filter_operation(stock))

    def test_market_leader_filter_operation__false__stock_is_not_market_leader(self):
        stock = mock.Mock(market_leader=lambda: False)

        self.assertFalse(market_leader_filter_operation(stock))

    def test_market_leader_enrich_operation(self):
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(update_report_in_metadata=update_report_in_metadata,
                          market_leader=lambda: "weird")

        market_leader_enrich_operation(stock)

        update_report_in_metadata.assert_called_with({
            "market_leader": "weird"
        })
