import unittest
from unittest import mock

from screener.filters.stock.metadata import minimum_weight, add_metadata, remove_metadata, cleanup_metadata


class MetadataTest(unittest.TestCase):
    def test_minimum_weight_return_true_when_greater_than_minimum_score(self):
        stock = mock.Mock(get_metadata=lambda: ({"satisfied_criteria": [1, 2, 3]}))

        self.assertTrue(minimum_weight(stock, 2))

    def test_minimum_weight_return_true_when_score_equal_to_minimum_score(self):
        stock = mock.Mock(get_metadata=lambda: ({"satisfied_criteria": [1, 2, 3]}))

        self.assertTrue(minimum_weight(stock, 3))

    def test_minimum_weight_return_false_when_score_less_than_minimum_score(self):
        stock = mock.Mock(get_metadata=lambda: ({"satisfied_criteria": [1, 2, 3]}))

        self.assertFalse(minimum_weight(stock, 4))

    @staticmethod
    def test_add_metadata_key_value():
        mocked_add_metadata = mock.Mock()
        stock = mock.Mock(add_metadata=mocked_add_metadata)

        add_metadata(stock, "fake", "property")

        mocked_add_metadata.assert_called_with("fake", "property")

    @staticmethod
    def test_remove_metadata():
        mocked_remove_metadata = mock.Mock()
        stock = mock.Mock(remove_metadata=mocked_remove_metadata)

        remove_metadata(stock, "fake")

        mocked_remove_metadata.assert_called_with("fake")

    @staticmethod
    def test_cleanup_metadata():
        mocked_cleanup_method = mock.Mock()
        stock = mock.Mock(cleanup_metadata=mocked_cleanup_method)

        cleanup_metadata(stock)

        mocked_cleanup_method.assert_called_with()
