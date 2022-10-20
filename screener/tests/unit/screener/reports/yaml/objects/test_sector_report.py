import unittest
from unittest import mock

from screener.common import u_yaml
from screener.reports.yaml.objects.sector_report import SectorReport


class SectorReportTest(unittest.TestCase):
    @mock.patch.object(u_yaml, "write")
    def test_generate(self, mocked_write):
        sector_report = SectorReport("out.yaml", ascending=True, sorted_by="k", keep_top_results=3)
        sector_report.generate([
            mock.Mock(to_dict=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 3}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{'k': 1}, {'k': 2}, {'k': 3}])

    @mock.patch.object(u_yaml, "write")
    def test_generate__in_reverse_order(self, mocked_write):
        index_report = SectorReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(to_dict=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 3}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5
        }, {
            'k': 4
        }, {
            'k': 3
        }])

    @mock.patch.object(u_yaml, "write")
    def test_generate__failed_to_to_dict(self, mocked_write):
        index_report = SectorReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(to_dict=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: 1 + [], get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5
        }, {
            'k': 4
        }, {
            'k': 2
        }])

    @mock.patch.object(u_yaml, "write")
    def test_generate__failed_field(self, mocked_write):
        index_report = SectorReport("out.yaml", ascending=False, sorted_by="k", keep_top_results=3)
        index_report.generate([
            mock.Mock(to_dict=lambda: {"k": 5}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 4}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 1}, get_current_value=lambda: 101),
            mock.Mock(to_dict=lambda: {"k": 2}, get_current_value=lambda: 101),
        ])
        mocked_write.assert_called_with("out.yaml", [{
            'k': 5
        }, {
            'k': 4
        }, {
            'k': 2
        }])
