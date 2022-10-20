# todo: fix reporting part

from screener.common import u_yaml
from screener.engine import Enrich
from screener.reports.yaml.common.grouping import Grouper
from screener.reports.yaml.common.sorting import Sorter


class Report:
    def __init__(self, output_file: str, operations: Enrich, sorter: Sorter = None, grouper: Grouper = None):
        self.output_file = output_file
        self._sorter = sorter
        self._grouper = grouper
        self._operations = operations

    def generate(self, stocks):
        self._operations.apply(stocks)
        stocks_metadata = [stock.get_metadata() for stock in stocks]
        sorted_stock = self._sorter.sort(stocks_metadata)
        report = self._grouper.group(sorted_stock)
        u_yaml.write(self.output_file, report)
