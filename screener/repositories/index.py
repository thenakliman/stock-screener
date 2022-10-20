from typing import Iterator

from screener.common.singleton_metaclass import Singleton
from screener.domain.fundamental.index import Index
from screener.factories.domain.index import get_index
from screener.repositories.mongodb import AppMongoClient
from screener.repositories.stock import StockRepository


class IndexRepository(metaclass=Singleton):
    INDEX_DOCS_NAME = "index"

    def __init__(self,
                 mongo_client: AppMongoClient,
                 stock_repository: StockRepository):
        self.mongodb_client = mongo_client
        self.stock_repository = stock_repository

    def get_all(self) -> Iterator[Index]:
        indexes = self.mongodb_client.find_all()
        indexes = map(self._update_stocks_in_index, indexes)
        return map(get_index, indexes)

    def _update_stocks_in_index(self, index: dict) -> dict:
        if "stocks" not in index:
            index["stocks"] = []
            return index

        stocks = []
        for isinid in index["stocks"]:
            stock = self.stock_repository.get_by_id(isinid)
            if stock is not None:
                stocks.append(stock)

        index["stocks"] = stocks
        return index
