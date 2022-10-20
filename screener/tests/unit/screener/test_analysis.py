import importlib
import unittest
from unittest import mock

from screener import screen
from screener.common import u_yaml
from screener.factories import engine as engine_factory
from screener.reports.yaml import sector
from screener.reports.yaml.factory import report as report_factory


class AnalysisTest(unittest.TestCase):
    @mock.patch.object(sector, "reporter")
    def test_analysis__analyse_sector(self, mocked_sector_analyser):
        importlib.reload(screen)
        args = mock.Mock(type="sector")
        screen.screen(args)

        mocked_sector_analyser.assert_called_with(args)

    @mock.patch.object(report_factory, "get_index_report")
    @mock.patch.object(u_yaml, "read", return_value="config")
    @mock.patch.object(engine_factory, "get_engine")
    @mock.patch("screener.screen.get_index_repository")
    def test_analyse_should_analyse_index(self, index_client_mock, engine_mock, mocked_u_yaml, mocked_index_report):
        get_all = mock.Mock(return_value=[1, 2, 3])
        index_client_mock.return_value = mock.Mock(get_all=get_all)
        run_mock_method = mock.Mock()
        engine_mock.return_value = mock.Mock(run=run_mock_method)
        mocked_index_report.return_value = mock.Mock(autospec=True)

        args = mock.Mock(type="index", output_file="out", config_file="config-file")
        screen.screen(args)

        get_all.assert_called_with()
        engine_mock.assert_called_with("config")
        run_mock_method.assert_called_with([1, 2, 3])
        mocked_index_report.assert_called_with("config", "out")
        mocked_u_yaml.assert_called_with("config-file")
        mocked_index_report.return_value.generate.asssert_called_with([1, 2, 3])

    @mock.patch.object(report_factory, "get_stock_report")
    @mock.patch.object(u_yaml, "read", return_value="config")
    @mock.patch.object(engine_factory, "get_engine")
    @mock.patch("screener.screen.get_stock_repository")
    def test_analyse_should_analyse_stock(self, stock_client_mock, engine_mock, mocked_u_yaml, mocked_stock_report):
        get_active_stocks = mock.Mock(return_value=[1, 2, 3])
        stock_client_mock.return_value = mock.Mock(get_active_stocks=get_active_stocks)
        run_mock_method = mock.Mock()
        engine_mock.return_value = mock.Mock(run=run_mock_method)
        mocked_stock_report.return_value = mock.Mock(autospec=True)

        args = mock.Mock(type="stock", output_file="out", config_file='config-file')
        screen.screen(args)

        engine_mock.assert_called_with("config")
        get_active_stocks.assert_called_with()
        engine_mock.assert_called_with("config")
        run_mock_method.assert_called_with([1, 2, 3])
        mocked_stock_report.assert_called_with("config", output_file="out")
        mocked_u_yaml.assert_called_with("config-file")
