from unittest import TestCase, mock

from screener.common import u_yaml
from screener.reports.yaml import stock


class StockReporterTest(TestCase):
    @mock.patch("screener.reports.yaml.stock.get_stock_repository")
    @mock.patch.object(u_yaml, "read")
    @mock.patch("screener.reports.yaml.stock.get_report")
    def test_stock_report(self, mocked_report_factory, mocked_yaml_read, mocked_stock_client):
        mocked_generate = mock.Mock()
        mocked_report_factory.return_value = mock.Mock(generate=mocked_generate)
        mocked_stock_client.return_value = mock.Mock(get_by_id=lambda x: {1: "a", 2: "b", 3: "c", 4: "d"}[x])
        config = {"companies": [1, 2, 3, 4]}
        mocked_yaml_read.return_value = config

        stock.reporter(mock.Mock(config_file="some-conf.yaml", output_file="some-output.yaml"))

        mocked_yaml_read.assert_called_with("some-conf.yaml")
        mocked_report_factory.assert_called_with(report_type="stock",
                                                 config=config,
                                                 output_file="some-output.yaml")
        mocked_generate.assert_called_with(["a", "b", "c", "d"])
