from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema

class CreateService(ABC):

    @abstractmethod
    def create(self, db: Session, new_customer: CustomerSchema):
        pass
