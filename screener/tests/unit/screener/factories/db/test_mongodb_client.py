from unittest import TestCase, mock
from unittest.mock import call

from screener.factories.repositories.mongodb_client import (
    get_institutional_investor_repository,
    get_stock_repository,
    get_index_repository,
    get_sector_repository
)


class MongoDbClientTest(TestCase):
    @mock.patch("screener.factories.repositories.mongodb_client.InstitutionalInvestorRepository")
    @mock.patch("screener.factories.repositories.mongodb_client.AppMongoClient", return_value="appmongo_client")
    @mock.patch("screener.factories.repositories.mongodb_client.MongoClient", return_value="mongoclient")
    def test_get_institutional_investor_client(self, mocked_mongo_db, mocked_app_mongo_client, ii_client):
        ii_client.INSTITUTIONAL_INVESTOR_NAME = "iid"
        ii_client.return_value = "ii"

        self.assertEqual("ii", get_institutional_investor_repository())

        mocked_mongo_db.assert_called_with(host="localhost", port=27017)
        mocked_app_mongo_client.assert_called_with(database_name='transformed-data', collection_name='iid',
                                                   mongo_client='mongoclient')
        ii_client.assert_called_with("appmongo_client")

    @mock.patch("screener.factories.repositories.mongodb_client.StockRepository")
    @mock.patch("screener.factories.repositories.mongodb_client.AppMongoClient", return_value="appmongo_client")
    @mock.patch("screener.factories.repositories.mongodb_client.MongoClient", return_value="mongoclient")
    def test_get_stock_client(self, mocked_mongo_db, mocked_app_mongo_client, stock_client):
        stock_client.STOCK_DOCS_NAME = "stock-docs"
        stock_client.return_value = "sc"

        self.assertEqual("sc", get_stock_repository())

        mocked_mongo_db.assert_called_with(host="localhost", port=27017)
        mocked_app_mongo_client.assert_called_with(database_name='transformed-data', collection_name='stock-docs',
                                                   mongo_client='mongoclient')
        stock_client.assert_called_with("appmongo_client")

    @mock.patch("screener.factories.repositories.mongodb_client.SectorRepository", return_value="sector-client")
    @mock.patch("screener.factories.repositories.mongodb_client.StockRepository", return_value="stock-client")
    @mock.patch("screener.factories.repositories.mongodb_client.AppMongoClient", return_value="appmongo_client")
    @mock.patch("screener.factories.repositories.mongodb_client.MongoClient", return_value="mongoclient")
    def test_get_sector_client(self,
                               mocked_mongo_db,
                               mocked_app_mongo_client,
                               mocked_stock_client,
                               mocked_sector_client):
        mocked_stock_client.STOCK_DOCS_NAME = "stock-docs"
        mocked_stock_client.return_value = "sc"

        self.assertEqual("sector-client", get_sector_repository())

        mocked_mongo_db.assert_called_with(host="localhost", port=27017)
        mocked_app_mongo_client.assert_called_with(database_name='transformed-data', collection_name='stock-docs',
                                                   mongo_client='mongoclient')
        mocked_stock_client.assert_called_with("appmongo_client")
        mocked_sector_client.assert_called_with("sc")

    @mock.patch("screener.factories.repositories.mongodb_client.IndexRepository")
    @mock.patch("screener.factories.repositories.mongodb_client.StockRepository")
    @mock.patch("screener.factories.repositories.mongodb_client.AppMongoClient", return_value="appmongo_client")
    @mock.patch("screener.factories.repositories.mongodb_client.MongoClient", return_value="mongoclient")
    def test_get_index_client(self, mocked_mongo_db,
                              mocked_app_mongo_client,
                              stock_client,
                              mocked_index_client):
        stock_client.STOCK_DOCS_NAME = "stock-docs"
        stock_client.return_value = "sc"
        mocked_index_client.return_value = "ic"
        mocked_index_client.INDEX_DOCS_NAME = "docs"

        self.assertEqual("ic", get_index_repository())

        mocked_mongo_db.assert_has_calls([call(host="localhost", port=27017), call(host="localhost", port=27017)])
        mocked_app_mongo_client.assert_has_calls([
            call(database_name='transformed-data', collection_name='docs', mongo_client='mongoclient'),
            call(database_name='transformed-data', collection_name='stock-docs', mongo_client='mongoclient')
        ])
        stock_client.assert_called_with("appmongo_client")
