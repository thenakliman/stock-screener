from unittest import TestCase, mock
from unittest.mock import patch, mock_open

from screener.common import u_yaml


class Test(TestCase):
    @mock.patch("screener.common.u_yaml.yaml")
    def test_read(self, mocked_yaml):
        mocked_yaml.safe_load = mock.Mock(return_value="data")
        filename = "data_file.yaml"
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            u_yaml.read(filename)
            mock_file.assert_called_with(filename, "r", encoding='utf-8')

        mocked_yaml.safe_load.assert_called()

    @mock.patch("screener.common.u_yaml.yaml")
    def test_write(self, mocked_yaml):
        mocked_yaml.safe_load = mock.Mock(return_value="data")
        filename = "data_file.yaml"
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            u_yaml.write(filename, "data")
            mock_file.assert_called_with(filename, "a", encoding='utf-8')

        mocked_yaml.dump.assert_called()
