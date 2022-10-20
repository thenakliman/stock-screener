from unittest import TestCase, mock

from screener.factories import engine as engine_factory
from screener.reports.yaml.common.formatter import Formatter
from screener.reports.yaml.common.grouping import Grouper
from screener.reports.yaml.factory.report import get_formatter, get_grouper, get_sorter, get_report


class ReportTest(TestCase):
    def test_get_formatter__when_format_is_defined(self):
        formatter = get_formatter("a")

        self.assertTrue(isinstance(formatter, Formatter))
        self.assertEqual("a", formatter._output_format)

    def test_get_formatter__default_value__when_format_is_not_defined(self):
        formatter = get_formatter()

        self.assertTrue(isinstance(formatter, Formatter))
        self.assertEqual(self._get_report_format(), formatter._output_format)

    @staticmethod
    def _get_report_format():
        return [
            "name",
            "sector",
            "score",
            "current_price",
            "less_than_maximum_price",
            "more_than_minimum_price",
            "pe",
            "industry_pe",
            "market_capital",
            "minimum_price",
            "price_to_book",
            "maximum_price",
            'industry_debt_to_equity',
            'industry_price_to_book_value',
            "latest_debt_to_equity",
            "satisfied_strategies",
            {
                "score_card": [
                    "net_sale",
                    "incomes",
                    "debt",
                    "debt_to_equity",
                    "long_term_debts",
                    "pe",
                    "industry_pe",
                    "not_met_criterias",
                    "met_criteria",
                    "isinid",
                    "market_leader",
                    "financial_year",
                    "asset_turnover",
                    "cash_flows",
                    "current_ratio",
                    "financial_year",
                    "graham_number",
                    "gross_margin",
                    "isinid",
                    "market_capital",
                    "name",
                    "new_issued_shares",
                    "operating_cash_flow",
                    "price_to_book",
                    "return_on_assets",
                    "tags",
                    "total_issued_shares",
                    "name",
                    "score",
                    "sector",
                    "more_than_minimum_price",
                    "less_than_maximum_price"
                ]
            }
        ]

    def test_get_grouper__when_format_is_defined(self):
        formatter = mock.Mock()
        grouper = get_grouper("a", 2, formatter)

        self.assertTrue(isinstance(grouper, Grouper))
        self.assertEqual(grouper._formatter, formatter)
        self.assertEqual("a", grouper._group_by)

    def test_get_grouper__default_value__when_format_is_not_defined(self):
        grouper = get_grouper("a", 4, None)

        self.assertTrue(isinstance(grouper, Grouper))
        self.assertTrue(isinstance(grouper._formatter, Formatter))
        self.assertEqual("a", grouper._group_by)

    def test_get_grouper__set_top_results(self):
        grouper = get_grouper("a", 3, None)

        self.assertTrue(isinstance(grouper, Grouper))
        self.assertTrue(isinstance(grouper._formatter, Formatter))
        self.assertEqual("a", grouper._group_by)
        self.assertEqual(3, grouper._keep_top_result)

    @mock.patch("screener.reports.yaml.factory.report.report_data_finder")
    @mock.patch("screener.reports.yaml.factory.report.Sorter", return_value="sorter")
    def test_get_sorter__default_value_decreasing__when_order_is_not_defined(self, mocked_sorter, mocked_report):
        sorter = get_sorter()

        self.assertEqual("sorter", sorter)
        mocked_sorter.assert_called_with(mocked_report, False, None)

    @mock.patch("screener.reports.yaml.factory.report.report_data_finder")
    @mock.patch("screener.reports.yaml.factory.report.Sorter", return_value="sorter")
    def test_get_sorter__default_value_decreasing__when_order_is_defined_descending(self, mocked_sorter, mocked_report):
        sorter = get_sorter(ascending=False)

        self.assertEqual("sorter", sorter)
        mocked_sorter.assert_called_with(mocked_report, False, None)

    @mock.patch("screener.reports.yaml.factory.report.report_data_finder")
    @mock.patch("screener.reports.yaml.factory.report.Sorter", return_value="sorter")
    def test_get_sorter__default_value_increasing__when_order_is_defined_ascending(self, mocked_sorter, mocked_report):
        sorter = get_sorter(ascending=True)

        self.assertEqual("sorter", sorter)
        mocked_sorter.assert_called_with(mocked_report, True, None)

    @mock.patch("screener.reports.yaml.factory.report.report_data_finder")
    @mock.patch("screener.reports.yaml.factory.report.Sorter", return_value="sorter")
    def test_get_sorter__define_group_by__create_object_with_sorted_by(self, mocked_sorter, mocked_report):
        sorter = get_sorter(sorted_by="a")

        self.assertEqual("sorter", sorter)
        mocked_sorter.assert_called_with(mocked_report, False, "a")

    @mock.patch.object(engine_factory, "get_operations", return_value="eng")
    @mock.patch("screener.reports.yaml.factory.report.report_data_finder")
    @mock.patch("screener.reports.yaml.factory.report.Sorter", return_value="sorter")
    @mock.patch("screener.reports.yaml.factory.report.Grouper", return_value="grouper")
    @mock.patch("screener.reports.yaml.factory.report.Formatter", return_value="formatter")
    @mock.patch("screener.reports.yaml.factory.report.Report", return_value="report")
    def test_get_report__stock_report(self,
                                      mocked_report,
                                      mocked_formatter,
                                      mocked_grouper,
                                      mocked_sorter,
                                      mocked_report_data_finder,
                                      mocked_get_engine_from_factory):
        config = {
            "output": {
                "sort": {
                    "by": "less_than_maximum",
                    "ascending": True
                },
                "group_by": "sector",
                "operations": [{"name": "of-type"}]
            }
        }

        report = get_report(report_type="stock", config=config, output_file="some.yaml")

        self.assertEqual("report", report)
        mocked_report.assert_called_with(
            output_file="some.yaml",
            sorter="sorter",
            grouper="grouper",
            operations="eng"
        )
        mocked_formatter.assert_called_with(self._get_report_format(), mocked_report_data_finder)
        mocked_grouper.asser_called_with("sector", mocked_report_data_finder, "formatter")
        mocked_sorter.assert_called_with(mocked_report_data_finder, True, "less_than_maximum")
        mocked_get_engine_from_factory.assert_called_with({
            'output': {
                'sort': {
                    'by': 'less_than_maximum',
                    'ascending': True
                },
                'group_by': 'sector',
                'operations': [{'name': 'of-type'}]}
        })

    @mock.patch("screener.reports.yaml.factory.report.IndexReport", return_value="index-report")
    def test_get_report__index_report(self, mocked_index_report):
        config = {
            "output": {
                "sort": {
                    "by": "less_than_maximum",
                    "ascending": True,
                    "keep_top_results": 3
                },
                "group_by": "sector",
                'operations': [{'name': 'of-type'}]
            }
        }

        report = get_report(report_type="index", config=config, output_file="some.yaml")

        self.assertEqual("index-report", report)
        mocked_index_report.assert_called_with(
            output_file="some.yaml",
            ascending=True,
            keep_top_results=3,
            sorted_by="less_than_maximum"
        )

    @mock.patch("screener.reports.yaml.factory.report.SectorReport", return_value="sector-report")
    def test_get_report__sector_report(self, mocked_index_report):
        config = {
            "output": {
                "sort": {
                    "by": "less_than_maximum",
                    "ascending": True,
                    "keep_top_results": 3
                },
                "group_by": "sector",
                'operations': [{'name': 'of-type'}]
            }
        }

        report = get_report(report_type="sector", config=config, output_file="some.yaml")

        self.assertEqual("sector-report", report)
        mocked_index_report.assert_called_with(
            output_file="some.yaml",
            ascending=True,
            keep_top_results=3,
            sorted_by="less_than_maximum"
        )

    def test_get_report__invalid_report__should_raise_exception(self):
        self.assertRaises(ValueError, lambda: get_report(report_type="invalid", config={}, output_file="some.yaml"))
