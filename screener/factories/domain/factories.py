from screener.common.constants import (
    InstitutionalInvestor
)
from screener.domain.fundamental.institutional_investor_activities import InstitutionalInvestorActivity


def get_institutional_investor_activity(institutional_investor) -> InstitutionalInvestorActivity:
    return InstitutionalInvestorActivity(
        _id=institutional_investor.get("_id"),
        date=institutional_investor.get("date"),
        investor_type=InstitutionalInvestor(institutional_investor.get("investor_type")),
        gross_purchase=institutional_investor.get("gross_purchase"),
        gross_sale=institutional_investor.get("gross_sale")
    )
