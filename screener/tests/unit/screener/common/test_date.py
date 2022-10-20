from unittest import TestCase, mock

from screener.common.date import (
    today,
    seconds_since_epoch,
    current_year, current_month
)


class DateTest(TestCase):
    @mock.patch("screener.common.date.datetime.date")
    def test_today(self, mocked_date):
        strftime = mock.Mock(return_value="some-date")
        mocked_date.today = mock.Mock(return_value=mock.Mock(strftime=strftime))

        date = today()

        self.assertEqual(date, "some-date")

        mocked_date.today.assert_called_with()
        strftime.assert_called_with("%d-%m-%Y")

    @mock.patch("screener.common.date.datetime.date")
    def test_year(self, mocked_date):
        mocked_date.today = mock.Mock(return_value=mock.Mock(year=2021))

        date = current_year()

        self.assertEqual(date, 2021)

        mocked_date.today.assert_called_with()

    @mock.patch("screener.common.date.datetime.date")
    def test_month(self, mocked_date):
        mocked_date.today = mock.Mock(return_value=mock.Mock(month=7))

        mon = current_month()

        self.assertEqual(mon, 7)

        mocked_date.today.assert_called_with()

    @mock.patch("screener.common.date.datetime.date")
    def test_seconds_since_epoch(self, mocked_date):
        mocked_date.today = mock.Mock(return_value=mock.Mock(strftime=lambda x: 123434 if x == "%s" else 0))

        seconds = seconds_since_epoch()

        self.assertEqual(123434, seconds)
