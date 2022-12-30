from typing import List, Dict

from screener.domain.fundamental.stock import Stock
from screener.filters.index.near_max_filter import WORKING_DAYS_IN_YEAR


class Sector:
    def __init__(self, name: str,
                 market_leader: Stock,
                 market_capital: int,
                 pe: float,
                 price_to_book: float,
                 asset_turn_over: float,
                 current_ratio: float,
                 gross_margin: float,
                 net_sales: List[Dict],
                 return_on_asset: float,
                 debt_to_equity: float,
                 historical_values: List[Dict],
                 stocks: List[Stock]):
        self._name = name
        self._stocks = stocks
        self._market_capital = market_capital
        self._market_leader = market_leader
        self._pe = pe
        self._price_to_book = price_to_book
        self._asset_turn_over = asset_turn_over
        self._current_ratio = current_ratio
        self._gross_margin = gross_margin
        self._net_sales = net_sales
        self._historical_values = historical_values
        self._return_on_asset = return_on_asset
        self._debt_to_equity = debt_to_equity
        self._metadata = {}

    def get_name(self) -> str:
        return self._name

    def get_market_capital(self) -> int:
        return self._market_capital

    def get_market_leader(self) -> Stock:
        return self._market_leader

    def get_stocks(self) -> List[Stock]:
        return self._stocks

    def get_pe(self) -> float:
        return self._pe

    def get_price_to_book_value(self) -> float:
        return self._price_to_book

    def get_asset_turnover(self) -> float:
        return self._asset_turn_over

    def get_current_ratio(self) -> float:
        return self._current_ratio

    def get_gross_margin(self) -> float:
        return self._gross_margin

    def get_return_on_asset(self) -> float:
        return self._return_on_asset

    def market_share_of_sale(self) -> List[Dict]:
        return [{
            stock.get_company_name(): stock.get_net_sales_for_year(
                stock.find_financial_year_of_latest_results())
        } for stock in self._stocks]

    def get_net_sales(self) -> List[Dict]:
        return self._net_sales

    def get_debt_to_equity(self) -> float:
        return self._debt_to_equity

    def update_report_in_metadata(self, key, value):
        if "report" in self._metadata:
            self._metadata["report"][key] = value
        else:
            self._metadata["report"] = {key: value}

    def get_metadata(self):
        return self._metadata

    def get_more_than_minimum_price(self, in_years=1.5):
        if len(self._historical_values) == 0:
            return 1000
        days_to_consider = int(in_years * WORKING_DAYS_IN_YEAR)
        days_to_consider = days_to_consider if len(self._historical_values) > days_to_consider else len(
            self._historical_values) - 1
        prices = [price["value"] for price in self._historical_values[-days_to_consider:]]

        minimum = min(prices)
        return (prices[0] - minimum) * 100 / minimum

    def get_less_than_maximum_price(self, in_years=1.5):
        if len(self._historical_values) == 0:
            return 1000

        days_to_consider = int(in_years * WORKING_DAYS_IN_YEAR)
        days_to_consider = days_to_consider if len(self._historical_values) > days_to_consider else len(
            self._historical_values) - 1
        prices = [price["value"] for price in self._historical_values[-days_to_consider:]]
        maximum = max(prices)
        return (maximum - prices[0]) * 100 / maximum

    def increase_in_sales(self, for_years):
        yearwise_increase_sales_ratio = []
        sales = sorted(self._net_sales, key=lambda sale: sale.get("year"), reverse=False)
        for index, sale in enumerate(sales[:-for_years + 1]):
            yearwise_increase_sales_ratio.append({
                "year": sales[index + 1].get("year"),
                "increase": (100 * (sales[index + 1].get("sale") - sale.get("sale", 1)) / (sale.get("sale", 1)))
            })

        return yearwise_increase_sales_ratio

    def to_dict(self):
        return {
            "name": self._name,
            "pe": self.get_pe(),
            "price_to_book": self.get_price_to_book_value(),
            "asset_turnover": self.get_asset_turnover(),
            "current_ratio": self.get_current_ratio(),
            "gross_margin": self.get_gross_margin(),
            "return_on_asset": self.get_return_on_asset(),
            "more_than_minimum": self.get_more_than_minimum_price(),
            "less_than_maximum": self.get_less_than_maximum_price()
        }
