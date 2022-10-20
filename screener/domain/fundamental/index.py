from typing import List

from screener.common import date, constants
from screener.common.u_dict import merge_dict
from screener.domain.technical.day_value import DayValue
from screener.domain.technical.historical_prices import HistoricalValues
from screener.domain.fundamental.stock import Stock
from screener.filters.stock.constants import ReportKeys


class Index:
    def __init__(self, name: str, stocks: List[Stock], historical_prices: HistoricalValues, current_value: float,
                 pe: float, pb: float, free_float: float, full: float, code: str, category: str = "",
                 date_created=None, last_date_updated=None):
        self._name = name
        self._stocks = stocks
        self._historical_values = historical_prices
        self._current_value = current_value
        self._pe = pe
        self._pb = pb
        self._free_float = free_float
        self._full = full
        self._date_created = date_created or date.today()
        self._last_date_updated = last_date_updated or date.today()
        self._category = category
        self._code = code
        self._metadata = {}

    def minimum_value_in_given_days(self, days: int) -> float:
        return self._historical_values.minimum_price_in_given_days(days)

    def maximum_value_in_given_days(self, days: int) -> float:
        return self._historical_values.maximum_price_in_given_days(days)

    def update_report_in_metadata(self, metadata: dict) -> None:
        merge_dict(self._metadata, metadata)

    def get_current_value(self) -> float:
        try:
            return float(self._historical_values.get_latest_price().get_value())
        except Exception:
            print(self._name, self._code)
        return -1

    def number_of_days_since_index_formed(self) -> int:
        return self._historical_values.number_of_days_stock_in_market()

    def get_stocks(self) -> List[Stock]:
        return self._stocks

    def get_name(self) -> str:
        return self._name

    def update_satisfied_strategy(self, flow_name: str) -> None:
        if ReportKeys.SATISFIED_STRATEGIES in self._metadata:
            self._metadata[ReportKeys.SATISFIED_STRATEGIES].append(flow_name)
        else:
            self._metadata[ReportKeys.SATISFIED_STRATEGIES] = [flow_name]

    def get_satisfied_strategies(self) -> List[str]:
        return self._metadata[ReportKeys.SATISFIED_STRATEGIES]

    def get_code(self) -> str:
        return self._code

    def get_category(self) -> str:
        return self._category

    def get_metadata(self) -> dict:
        return self._metadata

    def get_date_of_latest_available_value(self):
        return self._historical_values.get_date_of_latest_available_price()

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "stocks": [stock.get_isinid() for stock in self._stocks if stock is not None],
            "historical_values": self._historical_values.to_dict(),
            "current_value": self.get_current_value(),
            "pe": self._pe,
            "pb": self._pb,
            "free_float": self._free_float,
            "full": self._full,
            "code": self._code,
            "category": self._category,
            constants.DATE_CREATED: self._date_created,
            constants.LAST_DATE_UPDATED: self._last_date_updated,
            "_id": self._code
        }

    def update_historical_prices(self, latest_prices: List[DayValue]):
        self._historical_values.add_latest_price(latest_prices)
