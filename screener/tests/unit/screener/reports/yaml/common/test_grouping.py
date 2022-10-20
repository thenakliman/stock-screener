from unittest import TestCase, mock

from screener.reports.yaml.common.grouping import Grouper


class TestGrouper(TestCase):
    def test_group__when_there_are_no_group_by(self):
        def mocked_formatter(stock):
            return {"a": stock}

        formatter = mock.Mock(format=mocked_formatter)
        stock1 = {"key1": "value1"}
        stock2 = {"key2": "value2"}
        grouper = Grouper(None, mock.Mock(), formatter, 4).group([stock1, stock2])

        self.assertListEqual(grouper, [{"a": stock1}, {"a": stock2}])

    def test_group__group_stocks__when_only_one_stock(self):
        def mocked_formatter(stock):
            return {"a": stock}

        formatter = mock.Mock(format=mocked_formatter)
        stock = {"gp": "value2"}
        grouper = Grouper("gp", mock.Mock(find=lambda x, y: "value2"), formatter, 5).group([stock])

        self.assertDictEqual(grouper, {"value2": [{"a": stock}]})

    def test_group__group_stocks__when_only_multiple_stock(self):
        def mocked_formatter(stock):
            return {"a": stock}

        formatter = mock.Mock(format=mocked_formatter)
        stock1 = {"gp": "value1"}
        stock2 = {"gp": "value2"}
        grouper = Grouper("gp", mock.Mock(find=lambda x, y: "value2"), formatter, 4).group([stock1, stock2])

        self.assertDictEqual(grouper, {"value2": [{"a": stock1}, {"a": stock2}]})

    def test_group__group_stocks__when_multiple_groups(self):
        def mocked_formatter(stock):
            return {"a": stock}

        formatter = mock.Mock(format=mocked_formatter)
        stock1 = {"gp": "value1"}
        stock2 = {"gp": "value2"}
        grouper = Grouper("gp", mock.Mock(find=lambda x, y: y[x]), formatter, 2).group([stock1, stock2])

        self.assertDictEqual(grouper, {"value1": [{"a": stock1}], "value2": [{"a": stock2}]})

    def test_group__group_top_stocks__when_keep_top_results_is_defined(self):
        def mocked_formatter(stock):
            return {"a": stock}

        formatter = mock.Mock(format=mocked_formatter)
        stock1 = {"gp": "value1", 1: 2}
        stock2 = {"gp": "value1", 2: 3}
        stock3 = {"gp": "value3", 3: 2}
        stock4 = {"gp": "value3", 4: 1}
        stock5 = {"gp": "value1", 8: 2}
        grouper = Grouper("gp", mock.Mock(find=lambda x, y: y[x]), formatter, 2).group(
            [stock1, stock2, stock3, stock4, stock5])

        self.assertDictEqual(
            grouper, {
                "value1": [{"a": stock1}, {"a": stock2}],
                "value3": [{"a": stock3}, {"a": stock4}]
            }
        )
