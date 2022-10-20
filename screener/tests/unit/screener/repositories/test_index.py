from unittest import TestCase, mock

from screener.common.singleton_metaclass import Singleton
from screener.repositories.index import IndexRepository


class TestIndexClient(TestCase):
    def tearDown(self) -> None:
        Singleton._instances = {}

    @mock.patch("screener.repositories.index.get_index")
    def test_get_all_indexes(self, mocked_index):
        mocked_mongo_client = mock.Mock(find_all=lambda: [{"stocks": ["a"]}, {"stocks": ["b"]}])

        def get_by_id(stock):
            if stock == "a":
                return "__a"
            if stock == "b":
                return "__b"

        mocked_stock_client = mock.Mock(get_by_id=get_by_id)

        def _index_side_effect(index):
            if index["stocks"][0] == "__a":
                return "___a"
            elif index["stocks"][0] == "__b":
                return "___b"

        mocked_index.side_effect = _index_side_effect

        indexes = list(IndexRepository(mocked_mongo_client, mocked_stock_client).get_all())

        self.assertListEqual(["___a", "___b"], indexes)

    @mock.patch("screener.repositories.index.get_index")
    def test_get_all_indexes_when_stocks_does_not_exist_in_one_index(self, mocked_index):
        mocked_mongo_client = mock.Mock(
            find_all=lambda: [{"stocks": ["a"]}, {"stocks": ["b"]}, {"a": "b"}])

        def get_by_id(stock):
            if stock == "a":
                return "__a"
            if stock == "b":
                return "__b"

        mocked_stock_client = mock.Mock(get_by_id=get_by_id)

        def _index_side_effect(index):
            if len(index["stocks"]) == 0:
                return "__0"
            elif index["stocks"][0] == "__a":
                return "___a"
            elif index["stocks"][0] == "__b":
                return "___b"

        mocked_index.side_effect = _index_side_effect

        indexes = list(IndexRepository(mocked_mongo_client, mocked_stock_client).get_all())

        self.assertListEqual(["___a", "___b", "__0"], indexes)

    @mock.patch("screener.repositories.index.get_index")
    def test_get_all_indexes_when_one_company_code_does_not_exist(self, mocked_index):

        mocked_mongo_client = mock.Mock(find_all=lambda: [{"stocks": ["a"]}, {"stocks": ["b"]}])

        def get_by_id(stock):
            if stock == "a":
                return "__a"

        mocked_stock_client = mock.Mock(get_by_id=get_by_id)

        def _index_side_effect(index):
            if len(index["stocks"]) == 0:
                return "__none"
            if index["stocks"][0] == "__a":
                return "___a"
            if index["stocks"][0] == "__b":
                return "___b"

        mocked_index.side_effect = _index_side_effect

        indexes = list(IndexRepository(mocked_mongo_client, mocked_stock_client).get_all())

        self.assertListEqual(["___a", "__none"], indexes)
