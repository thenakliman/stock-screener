from typing import List


class Formatter:
    def __init__(self, output_format: List, report_data_finder):
        self._output_format = output_format
        self._report_data_finder = report_data_finder

    def format(self, metadata: dict):
        return self._format_report(self._output_format, metadata)

    def _format_report(self, report_format, metadata):
        formatted_report = {}
        for key in report_format:
            if isinstance(key, str):
                formatted_report[key] = self._report_data_finder.find(key, metadata)
            elif isinstance(key, dict):
                for k, v in key.items():
                    formatted_report[k] = self._format_report(v, metadata)
            else:
                raise ValueError()

        return formatted_report
