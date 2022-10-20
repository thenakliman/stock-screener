from unittest import TestCase, mock

from screener.common import u_yaml
from screener.reports.yaml.objects.stock_report import Report


class TestReport(TestCase):
    @mock.patch.object(u_yaml, "write")
    def test_generate(self, mocked_write):
        mocked_group = mock.Mock(return_value=[21, 22, 23])
        grouper = mock.Mock(group=mocked_group)
        mocked_sort = mock.Mock(return_value=[11, 12, 13])
        sorter = mock.Mock(sort=mocked_sort)
        engine = mock.Mock(autospec=True)
        report = Report("a.yaml", engine, sorter, grouper)

        stocks = [
            mock.Mock(get_metadata=lambda: 1),
            mock.Mock(get_metadata=lambda: 2),
            mock.Mock(get_metadata=lambda: 3)
        ]
        report.generate(stocks)
        mocked_sort.assert_called_with([1, 2, 3])
        mocked_group.assert_called_with([11, 12, 13])
        mocked_write.assert_called_with("a.yaml", [21, 22, 23])
        engine.apply.assert_called_with(stocks)
