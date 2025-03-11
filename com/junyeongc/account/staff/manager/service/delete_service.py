from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema


class DeleteService(ABC):

    @abstractmethod
    def delete(self, db: Session, user_id: str):
        pass

    
