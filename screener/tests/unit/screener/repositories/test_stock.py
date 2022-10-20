from unittest import TestCase, mock
from unittest.mock import call

from screener.common.singleton_metaclass import Singleton
from screener.repositories.stock import StockRepository


class TestStockClient(TestCase):
    def tearDown(self) -> None:
        Singleton._instances = {}

    @mock.patch("screener.repositories.stock.get_stock", return_value="stock")
    def test_get_stock(self, mocked_get_stock):
        find_by_id = mock.Mock(return_value="stock-details")
        app_mongo_client = mock.Mock(find_by_id=find_by_id)

        stock_object = StockRepository(app_mongo_client).get_by_id("isinid")

        self.assertEqual("stock", stock_object)
        find_by_id.assert_called_with("isinid")
        mocked_get_stock.assert_called_with("stock-details")

    def test_get_stock_when_stock_not_found(self):
        find_by_id = mock.Mock(return_value=None)
        app_mongo_client = mock.Mock(find_by_id=find_by_id)

        stock_object = StockRepository(app_mongo_client).get_by_id("isinid")

        self.assertIsNone(stock_object)
        find_by_id.assert_called_with("isinid")

    @mock.patch("screener.repositories.stock.get_stock")
    @mock.patch("screener.repositories.stock.update_sector_in_stocks")
    def test_get_active_stocks(self, update_sector_in_stocks, mocked_get_stock):
        mocked_get_active_stocks = mock.Mock(return_value=[None, 1, None, 2, 3])
        app_mongo_client = mock.Mock(find_all_by_query=mocked_get_active_stocks)
        mocked_get_stock.side_effect = lambda x: {1: 1, 2: 2, 3: 3}[x]

        stocks = StockRepository(app_mongo_client).get_active_stocks()

        self.assertEqual([1, 2, 3], stocks)
        mocked_get_stock.assert_has_calls([call(1), call(2), call(3)])
        update_sector_in_stocks.assert_called_with([1, 2, 3])
