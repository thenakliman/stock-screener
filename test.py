from unittest import mock

from screener.analysis.analysis import analysis

analysis(mock.Mock(dimension="stock", config_file="config/stock-good-fundamental.yaml", output_file="output.yml"))