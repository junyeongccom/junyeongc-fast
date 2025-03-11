from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema
from com.junyeongc.climate.service.create_service import CreateService


class DefaultCreateRepository(CreateService):
    def create(self, db: Session, new_customer: CustomerSchema):
        print("😃😃Repository new_customer wjdqh:", new_customer)
        pass

class ValidatedCreateRepository(CreateService):
    def create(self, db: Session, new_customer: CustomerSchema):
        pass