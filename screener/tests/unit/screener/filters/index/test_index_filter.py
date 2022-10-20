import unittest
from unittest import mock

from screener.filters.index.index_filter import index_filter_operation, index_enrich_operation


class IndexFilterTest(unittest.TestCase):
    def test_index_filter_operation_should_return_true_when_index_match(self):
        self.assertTrue(index_filter_operation(
            mock.Mock(get_name=lambda: "jai-ho"),
            ["jai", "ho", "jainaho", "jai-ho", "cool-ho"]))

    def test_index_filter_operation_should_return_false_when_index_match(self):
        self.assertFalse(index_filter_operation(
            mock.Mock(get_name=lambda: "jangli"),
            ["jai", "ho", "jainaho", "jai-ho", "cool-ho"]))

    @staticmethod
    def test_index_enrich_operation_should_return_false_when_index_match():
        update_report_in_metadata = mock.Mock()

        index_enrich_operation(mock.Mock(
            get_name=lambda: "jangli",
            update_report_in_metadata=update_report_in_metadata))

        update_report_in_metadata.assert_called_with({"name": "jangli"})
