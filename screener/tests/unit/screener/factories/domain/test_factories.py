from unittest import TestCase, mock

from screener.common.constants import InstitutionalInvestor
from screener.factories.domain.factories import get_institutional_investor_activity


class TestFactories(TestCase):
    @mock.patch("screener.factories.domain.factories.InstitutionalInvestorActivity", return_value="i-n")
    def test_get_institutional_investor_activity(self, mocked_iia):
        institutional_investor = get_institutional_investor_activity({
            "_id": "i-d",
            "date": "12-01-2020",
            "investor_type": "FII",
            "gross_purchase": 2323,
            "gross_sale": 5453
        })

        self.assertEquals(institutional_investor, "i-n")
        mocked_iia.assert_called_with(_id="i-d",
                                      date="12-01-2020",
                                      investor_type=InstitutionalInvestor.FII,
                                      gross_purchase=2323,
                                      gross_sale=5453)
