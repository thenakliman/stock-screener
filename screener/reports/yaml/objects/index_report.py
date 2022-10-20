# todo: fix reporting part
from screener.common import u_yaml


class IndexReport:
    def __init__(self, output_file, ascending=False, sorted_by=None, keep_top_results=None):
        self._ascending = ascending
        self._sorted_by = sorted_by or "more_than_minimum_price"
        self.output_file = output_file
        self._keep_top_results = keep_top_results

    def _comparator(self, index_report):
        try:
            return index_report[self._sorted_by]
        except KeyError:
            print(f"failed to get {self._sorted_by} parameter")

        return 0

    @staticmethod
    def _format_report(index):
        try:
            metadata = index.get_metadata()
            metadata["current_value"] = index.get_current_value()
            return metadata
        except Exception as e:
            print("failed to retrieve metdata", e)
            return None

    def generate(self, indexes):
        indexes_report = filter(lambda x: x is not None, map(IndexReport._format_report, indexes))
        sorted_indexes = sorted(
            indexes_report,
            key=self._comparator,
            reverse=not self._ascending)[:self._keep_top_results]
        u_yaml.write(self.output_file, sorted_indexes)
