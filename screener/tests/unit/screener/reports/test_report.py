import importlib
from unittest import TestCase, mock

from screener.reports import report
from screener.reports.yaml import stock, sector, index


class ReporterTest(TestCase):
    @mock.patch.object(index, "reporter")
    @mock.patch.object(sector, "reporter")
    @mock.patch.object(stock, "reporter")
    def test_reporter__index(self,
                             mocked_stock_report,
                             mocked_sector_report,
                             mocked_index_report):
        args = mock.Mock(type="index")
        importlib.reload(report)
        report.reporter(args)

        mocked_index_report.assert_called_with(args)

    @mock.patch.object(index, "reporter")
    @mock.patch.object(sector, "reporter")
    @mock.patch.object(stock, "reporter")
    def test_reporter__sector(self,
                              mocked_stock_report,
                              mocked_sector_report,
                              mocked_index_report):
        args = mock.Mock(type="sector")
        importlib.reload(report)
        report.reporter(args)

        mocked_sector_report.assert_called_with(args)

    @mock.patch.object(index, "reporter")
    @mock.patch.object(sector, "reporter")
    @mock.patch.object(stock, "reporter")
    def test_reporter__stock(self,
                             mocked_stock_report,
                             mocked_sector_report,
                             mocked_index_report):
        args = mock.Mock(type="stock")
        importlib.reload(report)
        report.reporter(args)

        mocked_stock_report.assert_called_with(args)
