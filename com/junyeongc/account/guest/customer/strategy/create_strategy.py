from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema
from com.junyeongc.climate.service.create_service import CreateService


class DefaultCreateStrategy(CreateService):
    def create(self, db: Session, new_customer: CustomerSchema):
        customer_repo = DefaultCreateStrategy(db)
        return customer_repo.create(new_customer)

class ValidatedCreateStrategy(CreateService):
    def create(self, db: Session, new_customer: CustomerSchema):
        pass