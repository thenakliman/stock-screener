import unittest
from unittest import mock

from screener.exceptions.not_found import YearNotFound, DataNotFound
from screener.filters.base import apply_operation_by_years


class BaseTest(unittest.TestCase):
    @staticmethod
    def test_apply_operation_by_years__when_no_years():
        callable_ = mock.Mock()

        apply_operation_by_years(callable_, [])

        callable_.assert_not_called()

    def test_apply_operation_by_years__when_years_are_given(self):
        results = apply_operation_by_years(lambda x: x * x, [1, 2, 3])

        self.assertListEqual(results, [1, 4, 9])

    def test_apply_operation_by_years__when_data_is_not_present(self):
        def _method(d):
            raise DataNotFound()

        results = apply_operation_by_years(_method, [1, 2, 3])

        self.assertListEqual([], results)

    def test_apply_operation_by_years__when_operation_fails_for_years(self):
        def _side_effect(year):
            if year == 2:
                raise YearNotFound(year=2)

            return year * year

        results = apply_operation_by_years(_side_effect, [1, 2, 3])

        self.assertListEqual(results, [1, 9])

    def test_apply_operation_by_years__when_operation_raise_exception(self):
        def _side_effect(year):
            if year == 2:
                raise ValueError

            return year * year

        results = apply_operation_by_years(_side_effect, [1, 2, 3])

        self.assertListEqual(results, [1, 9])
