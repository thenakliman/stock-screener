from unittest import TestCase, mock

from screener.exceptions.not_found import ReportDataNotFound
from screener.reports.yaml.common.sorting import Sorter


class TestSorter(TestCase):
    def test_sort__ascending(self):
        report_data_finder = mock.Mock(find=lambda k, x: x[k])
        self.sorter = Sorter(report_data_finder, ascending=True, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"paisa": 321}, {"paisa": 13}, {"paisa": 33}])

        self.assertListEqual([{'paisa': 13}, {'paisa': 33}, {'paisa': 321}, {'paisa': 3213}], sorted_list)

    def test_sort__descending(self):
        report_data_finder = mock.Mock(find=lambda k, x: x[k])
        self.sorter = Sorter(report_data_finder, ascending=False, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"paisa": 321}, {"paisa": 13}, {"paisa": 33}])

        self.assertListEqual([{'paisa': 3213}, {'paisa': 321}, {'paisa': 33}, {'paisa': 13}], sorted_list)

    def test_sort__ascending__key_does_not_exist(self):
        def find(k, x):
            if k not in x:
                raise ReportDataNotFound(data="some")
            return x[k]

        report_data_finder = mock.Mock(find=find)
        self.sorter = Sorter(report_data_finder, ascending=False, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"value": 321}, {"paisa": 13}, {"paisa": 33}])

        self.assertListEqual([{'paisa': 3213}, {'paisa': 33}, {'paisa': 13}, {'value': 321}], sorted_list)

    def test_sort__descending__key_does_not_exist(self):
        def find(k, x):
            if k not in x:
                raise ReportDataNotFound(data="some")
            return x[k]

        report_data_finder = mock.Mock(find=find)
        self.sorter = Sorter(report_data_finder, ascending=True, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"paisa": 321}, {"paisa": 13}, {"value": 33}])

        self.assertListEqual([{'value': 33}, {'paisa': 13}, {'paisa': 321}, {'paisa': 3213}], sorted_list)

    def test_sort__ascending__value_is_none(self):
        def find(k, x):
            if k not in x:
                return None
            return x[k]

        report_data_finder = mock.Mock(find=find)
        self.sorter = Sorter(report_data_finder, ascending=False, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"value": 321}, {"paisa": 13}, {"paisa": 33}])

        self.assertListEqual([{'paisa': 3213}, {'paisa': 33}, {'paisa': 13}, {'value': 321}], sorted_list)

    def test_sort__descending__value_is_none(self):
        def find(k, x):
            if k not in x:
                return None
            return x[k]

        report_data_finder = mock.Mock(find=find)
        self.sorter = Sorter(report_data_finder, ascending=True, sorted_by="paisa")
        sorted_list = self.sorter.sort([{"paisa": 3213}, {"paisa": 321}, {"paisa": 13}, {"value": 33}])

        self.assertListEqual([{'value': 33}, {'paisa': 13}, {'paisa': 321}, {'paisa': 3213}], sorted_list)
