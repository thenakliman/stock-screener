class AppMongoClient:
    def __init__(self, database_name, collection_name: str, mongo_client):
        self.client = mongo_client
        self.db = getattr(getattr(self.client, database_name), collection_name)

    def insert(self, data):
        return self.db.insert_one(data)

    def insert_all(self, data):
        return self.db.insert_many(data)

    def find_by_id(self, id_):
        return self.db.find_one({"_id": id_})

    def find(self, key, value):
        return self.db.find_one({key: value})

    def find_all(self):
        return self.db.find({})

    def find_all_by_query(self, query):
        return self.db.find(query)

    def find_all_fields(self, fields):
        return self.db.find({}, fields)

    def delete_all_by_id(self, ids):
        return self.db.delete_many({"_id": {"$in": ids}})

    def delete_by_id(self, id_):
        return self.db.delete_one({"_id": id_})

    def close(self):
        self.client.close()

    def replace(self, id_, stock_details):
        return self.db.replace_one({"_id": id_}, stock_details)

    def distinct(self, key):
        return self.db.distinct(key)
