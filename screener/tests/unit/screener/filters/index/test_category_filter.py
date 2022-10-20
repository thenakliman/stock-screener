import unittest
from unittest import mock

from screener.filters.index.category_filter import category_filter_operation, category_enrich_operation


class CategoryFilterTest(unittest.TestCase):
    def test_category_filter__true__when_category_match(self):
        self.assertTrue(category_filter_operation(mock.Mock(get_category=lambda: "fmcg"), "fmcg"))

    def test_category_filter__false__when_category_does_not_match(self):
        self.assertFalse(category_filter_operation(mock.Mock(get_category=lambda: "fmcg"), "fmcg1"))

    def test_index_enrich_operation_should_return_false_when_index_match(self):
        update_report_in_metadata = mock.Mock()

        category_enrich_operation(mock.Mock(
            get_category=lambda: "jangli",
            update_report_in_metadata=update_report_in_metadata))

        update_report_in_metadata.assert_called_with({"category": "jangli"})
