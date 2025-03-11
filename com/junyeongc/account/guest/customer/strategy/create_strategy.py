from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema
from com.junyeongc.account.guest.customer.service.create_service import CreateService


class DefaultCreateStrategy(CreateService):
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        customer_repo = DefaultCreateStrategy(db)
        return customer_repo.create(new_customer)

class ValidatedCreateStrategy(CreateService):
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        AsyncSession