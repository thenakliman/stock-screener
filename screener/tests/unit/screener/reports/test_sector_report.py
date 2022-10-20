from unittest import TestCase, mock

from screener.common import u_yaml
from screener.reports.yaml import sector


class StockReporterTest(TestCase):
    @mock.patch("screener.reports.yaml.sector.get_sector_repository")
    @mock.patch.object(u_yaml, "read")
    @mock.patch("screener.reports.yaml.sector.get_report")
    def test_sector_report(self, mocked_report_factory, mocked_yaml_read, mocked_sector_client):
        mocked_generate = mock.Mock()
        mocked_report_factory.return_value = mock.Mock(generate=mocked_generate)
        mocked_sector_client.return_value = mock.Mock(get_all_sectors=lambda: ['s1', 's2'])
        config = {"companies": [1, 2, 3, 4]}
        mocked_yaml_read.return_value = config

        sector.reporter(mock.Mock(config_file="some-conf.yaml", output_file="some-output.yaml"))

        mocked_yaml_read.assert_called_with("some-conf.yaml")
        mocked_report_factory.assert_called_with(report_type="sector",
                                                 config=config,
                                                 output_file="some-output.yaml")
        mocked_generate.assert_called_with(['s1', 's2'])
