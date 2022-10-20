from unittest import TestCase, mock

from screener.common.singleton_metaclass import Singleton
from screener.repositories.mongodb import AppMongoClient


class TestAppMongoClient(TestCase):
    def setUp(self):
        self.collection = mock.Mock(posts=mock.Mock())
        database = mock.Mock(collection=self.collection, close=mock.Mock())
        self.pymongo = mock.Mock(database=database)
        self.mongo_client = AppMongoClient("database", "collection", self.pymongo)
        Singleton._instances = {}

    def test_insert_one(self):
        record = "inserted-record"
        self.collection.insert_one = mock.Mock(return_value=record)

        data = {"a": "b"}
        inserted_record = self.mongo_client.insert(data)

        self.assertEqual(record, inserted_record)
        self.collection.insert_one.assert_called_with(data)

    def test_insert_all(self):
        record = "inserted-record"
        self.collection.insert_many = mock.Mock(return_value=record)

        data = {"a": "b"}
        inserted_record = self.mongo_client.insert_all(data)

        self.assertEqual(record, inserted_record)
        self.collection.insert_many.assert_called_with(data)

    def test_find_by_id(self):
        record = "inserted-record"
        self.collection.find_one = mock.Mock(return_value=record)

        data = {"a": "b"}
        inserted_record = self.mongo_client.find_by_id(data)

        self.assertEqual(record, inserted_record)
        self.collection.find_one.assert_called_with({"_id": data})

    def test_find(self):
        record = "inserted-record"
        self.collection.find_one = mock.Mock(return_value=record)

        data = {"a": "b"}
        inserted_record = self.mongo_client.find("key", data)

        self.assertEqual(record, inserted_record)
        self.collection.find_one.assert_called_with({"key": data})

    def test_find_all(self):
        record = "inserted-record"
        self.collection.find = mock.Mock(return_value=record)

        inserted_record = self.mongo_client.find_all()

        self.assertEqual(record, inserted_record)
        self.collection.find.assert_called_with({})

    def test_delete_by_id(self):
        record = "inserted-record"
        self.collection.delete_one = mock.Mock(return_value=record)

        inserted_record = self.mongo_client.delete_by_id("id")

        self.assertEqual(record, inserted_record)
        self.collection.delete_one.assert_called_with({'_id': 'id'})

    def test_delete_all_by_id(self):
        record = "deleted-record"
        self.collection.delete_many = mock.Mock(return_value=record)

        deleted = self.mongo_client.delete_all_by_id(["id"])

        self.assertEqual(record, deleted)
        self.collection.delete_many.assert_called_with({"_id": {"$in": ["id"]}})

    def test_find_all_by_query(self):
        record = "records"
        self.collection.find = mock.Mock(return_value=record)

        results = self.mongo_client.find_all_by_query({"active": True})

        self.assertEqual(record, results)
        self.collection.find.assert_called_with({"active": True})

    def test_replace(self):
        record = "inserted-record"
        self.collection.replace_one = mock.Mock(return_value=record)

        inserted_record = self.mongo_client.replace({"_id": "data"}, record)

        self.assertEqual(record, inserted_record)
        self.collection.replace_one.assert_called_with({'_id': {'_id': 'data'}}, inserted_record)

    def test_find_all_fields(self):
        record = "record"
        self.collection.find = mock.Mock(return_value=record)

        inserted_record = self.mongo_client.find_all_fields({"data": 1})

        self.assertEqual(record, inserted_record)
        self.collection.find.assert_called_with({}, {"data": 1})

    def test_distinct(self):
        record = [1, 2, 3, 4]
        self.collection.distinct = mock.Mock(return_value=record)

        distinct_record = self.mongo_client.distinct("data")

        self.assertListEqual(record, distinct_record)
        self.collection.find.distinct("data")

    def test_close(self):
        self.mongo_client.close()

        self.pymongo.close.assert_called_with()
