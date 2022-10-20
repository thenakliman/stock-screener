import unittest
from unittest import mock

from screener.common import u_yaml
from screener.reports.yaml.objects.index_report import IndexReport


class IndexReportTest(unittest.TestCase):
    @mock.patch.object(u_yaml, "write")
    def test_generate(self, mocked_write):
        index_report = IndexReport("out.yaml", ascending=True, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(get_metadata=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 3}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 1, 'current_value': 101
        }, {
            'k': 2, 'current_value': 101
        }, {
            'k': 3, 'current_value': 101
        }])

    @mock.patch.object(u_yaml, "write")
    def test_generate__in_reverse_order(self, mocked_write):
        index_report = IndexReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(get_metadata=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 3}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5, 'current_value': 101
        }, {
            'k': 4, 'current_value': 101
        }, {
            'k': 3, 'current_value': 101
        }])

    @mock.patch.object(u_yaml, "write")
    def test_generate__failed_to_get_metadata(self, mocked_write):
        index_report = IndexReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(get_metadata=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: 1 + [], get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5, 'current_value': 101
        }, {
            'k': 4, 'current_value': 101
        }, {
            'k': 2, 'current_value': 101
        }])

    @mock.patch.object(u_yaml, "write")
    def test_generate__failed_field(self, mocked_write):
        index_report = IndexReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(get_metadata=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(get_metadata=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5, 'current_value': 101
        }, {
            'k': 4, 'current_value': 101
        }, {
            'k': 2, 'current_value': 101
        }])
