from unittest import TestCase

from screener.common.constants import InstitutionalInvestor
from screener.domain.fundamental.institutional_investor_activities import InstitutionalInvestorActivity


class TestInstitutionalInvestorActivity(TestCase):
    def test_to_dict(self):
        institutional_investor = InstitutionalInvestorActivity(
            "i-d",
            "12-12-2010",
            InstitutionalInvestor.FII,
            1200,
            3211
        )

        self.assertDictEqual({
            "_id": "i-d",
            "gross_purchase": 1200,
            "gross_sale": 3211,
            "investor_type": "FII",
            "date": "12-12-2010"
        }, institutional_investor.to_dict())
