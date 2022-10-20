from typing import Optional, List

from screener.factories.domain.factories import get_institutional_investor_activity
from screener.domain.fundamental.institutional_investor_activities import InstitutionalInvestorActivity


class InstitutionalInvestorRepository:
    INSTITUTIONAL_INVESTOR_NAME = "institutional_investor"

    def __init__(self, mongodb_client):
        self.mongodb_client = mongodb_client

    def save(self, institutional_investor: InstitutionalInvestorActivity):
        institutional_investor_as_dict = institutional_investor.to_dict()
        del institutional_investor_as_dict["_id"]
        return self.mongodb_client.insert(institutional_investor_as_dict)

    def get_all(self) -> List[InstitutionalInvestorActivity]:
        institutional_investors = self.mongodb_client.find_all()
        return [get_institutional_investor_activity(institutional_investor)
                for institutional_investor in institutional_investors]

    def get_by_id(self, id_: str) -> Optional[InstitutionalInvestorActivity]:
        institutional_investor = self.mongodb_client.find_by_id(id_)
        if institutional_investor is None:
            return None

        return get_institutional_investor_activity(institutional_investor)
