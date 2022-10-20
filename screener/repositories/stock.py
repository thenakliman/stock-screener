from typing import Optional, List

from screener.common.singleton_metaclass import Singleton
from screener.domain.fundamental.stock import Stock
from screener.factories.domain.sector import update_sector_in_stocks
from screener.factories.domain.stock import get_stock
from screener.repositories.mongodb import AppMongoClient


class StockRepository(metaclass=Singleton):
    STOCK_DOCS_NAME = "stock"

    def __init__(self, mongo_client: AppMongoClient):
        self.stock_client = mongo_client

    def get_by_id(self, isinid: str) -> Optional[Stock]:
        stock_details = self.stock_client.find_by_id(isinid)
        if stock_details is None:
            return None

        return get_stock(stock_details)

    def get_active_stocks(self) -> List[Stock]:
        stocks = [
            get_stock(stock_details) for stock_details in self.stock_client.find_all_by_query({"active": True})
            if stock_details is not None
        ]
        update_sector_in_stocks(stocks)
        return stocks
