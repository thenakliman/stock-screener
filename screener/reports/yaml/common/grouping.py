from typing import List

from screener.reports.yaml.common.formatter import Formatter


class Grouper:
    def __init__(self, group_by: str, report_data_finder, formatter: Formatter, keep_top_result: int):
        self._group_by = group_by
        self._keep_top_result = keep_top_result
        self._report_data_finder = report_data_finder
        self._formatter = formatter

    def group(self, stocks: List[dict]):
        if self._group_by is None:
            return [self._formatter.format(stock) for stock in stocks]

        report = {}
        for stock in stocks:
            group_key = self._report_data_finder.find(self._group_by, stock)
            formatted_stock_report = self._formatter.format(stock)
            if group_key in report:
                if len(report[group_key]) < self._keep_top_result:
                    report[group_key].append(formatted_stock_report)
            else:
                report[group_key] = [formatted_stock_report]

        return report
