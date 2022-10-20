from unittest import TestCase, mock
from unittest.mock import call

from screener.reports.yaml.common.formatter import Formatter


class TestFormatter(TestCase):
    def test_format__format__for_a_key(self):
        mocked_find = mock.Mock(return_value=10)
        report_data_finder = mock.Mock(find=mocked_find)
        formatter = Formatter(["some"], report_data_finder)

        formatted_output = formatter.format({"some": 10, id: 1})

        self.assertEqual(formatted_output, {"some": 10})

    def test_format__format__for_multiple_keys(self):
        def side_effect(k, x):
            if k == "some":
                return 10
            elif k == "oKey":
                return 30

        mocked_find = mock.Mock(side_effect=side_effect)
        report_data_finder = mock.Mock(find=mocked_find)
        formatter = Formatter(["some", "oKey"], report_data_finder)

        source_obj = {"some": 10, "oKey": 1}
        formatted_output = formatter.format(source_obj)

        self.assertEqual(formatted_output, {"some": 10, "oKey": 30})
        mocked_find.assert_has_calls([call("some", source_obj), call("oKey", source_obj)])

    def test_format__raise_exception__for_integer_key(self):
        formatter = Formatter([101], mock.Mock())

        source_obj = {"some": 10, "oKey": 1}
        with self.assertRaises(ValueError):
            formatter.format(source_obj)

    def test_format__raise_exception__when_dictionary_in_format(self):
        def side_effect(k, x):
            if k == "someKey":
                return 10
            elif k == "key":
                return 30

        mocked_find = mock.Mock(side_effect=side_effect)
        report_data_finder = mock.Mock(find=mocked_find)
        formatter = Formatter(["someKey", {"other": ["key"]}], report_data_finder).format({"some": 10, "key": 1})

        self.assertDictEqual(formatter, {"other": {"key": 30}, "someKey": 10})

    def test_format__raise_exception__when_multiple_key_in_dictionary(self):
        def side_effect(k, x):
            if k == "someKey":
                return 10
            elif k == "key":
                return 30
            elif k == "weird":
                return 34

        mocked_find = mock.Mock(side_effect=side_effect)
        report_data_finder = mock.Mock(find=mocked_find)
        formatter = Formatter(
            ["someKey", {"other": ["key", "weird"]}], report_data_finder).format({"some": 10, "key": 1})

        self.assertDictEqual(formatter, {"other": {"key": 30, "weird": 34}, "someKey": 10})
