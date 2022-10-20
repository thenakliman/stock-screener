from typing import List

from screener.exceptions.not_found import ReportDataNotFound


class Sorter:
    def __init__(self, report_data_finder, ascending: bool = False, sorted_by: str = None):
        self._report_data_finder = report_data_finder
        self._ascending = ascending
        self._sorted_by = sorted_by

    def sort(self, stocks: List[dict]):
        return sorted(
            stocks,
            key=self._comparator,
            reverse=not self._ascending)

    def _comparator(self, stock):
        try:
            return self._report_data_finder.find(self._sorted_by, stock) or 0
        except ReportDataNotFound as e:
            print(e)
            return 0
