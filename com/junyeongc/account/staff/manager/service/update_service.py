from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema


class UpdateService(ABC):

    @abstractmethod
    def update(self, db: Session, update_customer: CustomerSchema):
        pass
