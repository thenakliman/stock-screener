import traceback
from abc import abstractmethod
from typing import List

from screener.domain.fundamental.stock import Stock
from screener.exceptions.not_found import DataNotFound


class Engine:
    def __init__(self, strategies):
        self._strategies = strategies

    def run(self, stocks):
        return self._strategies.apply(stocks)


class Operations:
    @abstractmethod
    def apply(self, stocks):
        pass


class Filter(Operations):
    def __init__(self, filter_operations):
        self._filter_operations = filter_operations

    def apply(self, stocks):
        return filter(self._pass_filters, stocks)

    def _pass_filters(self, stock):
        for filter_operation in self._filter_operations:
            try:
                if filter_operation(stock) is False:
                    return False
            except DataNotFound:
                print(f"Data not found for isinid={stock.get_isinid()}")
                return False
            except Exception as e:
                print(e)
                traceback.print_exc()
                return False

        return True


class Enrich(Operations):
    def __init__(self, enrich_operations):
        self._enrich_operations = enrich_operations

    def apply(self, stocks):
        return [self._apply_operation(stock) for stock in stocks]

    def _apply_operation(self, stock):
        for _enrich_operation in self._enrich_operations:
            try:
                _enrich_operation(stock)
            except DataNotFound:
                print(f"Data not found for isinid={stock.get_isinid()}")
            except Exception as e:
                print(e)
                traceback.print_exc()

        return stock


class Strategy:
    def __init__(self, name: str, operations: List[Operations]):
        self._name = name
        self._operations = operations

    def apply(self, stocks: List[Stock]):
        for operation in self._operations:
            stocks = list(operation.apply(stocks))

        list(map(lambda stock: stock.update_satisfied_strategy(self._name), stocks))
        return stocks


class Strategies:
    def __init__(self, strategies: List[Strategy]):
        self._strategies = strategies

    def apply(self, stocks: List[Stock]):
        unique_stocks = set()
        for strategy in self._strategies:
            filtered_stocks = strategy.apply(stocks)
            unique_stocks.update(filtered_stocks)

        return unique_stocks
