from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.model.customer_entity import CustomerEntity
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema
from com.junyeongc.climate.service.create_service import CreateService


class DefaultCreateRepository(CreateService):
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        print("😃😃Repository new_customer wjdqh:", new_customer)
        db.add(CustomerEntity(
            user_id = new_customer.user_id,
            name = new_customer.name,
            password = new_customer.password,
            email = new_customer.email
        ))
        db.commit()
        db.refresh(new_customer)
        return new_customer
        
class ValidatedCreateRepository(CreateService):
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        pass