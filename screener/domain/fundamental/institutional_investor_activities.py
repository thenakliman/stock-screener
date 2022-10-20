from screener.common.constants import (
    InstitutionalInvestor,
    GROSS_PURCHASE_KEY,
    GROSS_SALE_KEY,
    DATE_KEY
)


class InstitutionalInvestorActivity:
    def __init__(self,
                 _id: str,
                 date: str,
                 investor_type: InstitutionalInvestor,
                 gross_purchase: float,
                 gross_sale: float):
        self.id = _id
        self._date = date
        self._investor_type = investor_type
        self._gross_purchase = gross_purchase
        self._gross_sale = gross_sale

    def to_dict(self):
        return {
            "_id": self.id,
            GROSS_PURCHASE_KEY: self._gross_purchase,
            GROSS_SALE_KEY: self._gross_sale,
            "investor_type": self._investor_type.value,
            DATE_KEY: self._date
        }
