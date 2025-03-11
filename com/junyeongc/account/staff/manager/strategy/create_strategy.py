from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.staff.manager.model.manager_schema import ManagerSchema
from com.junyeongc.account.staff.manager.service.create_service import CreateService

class DefaultCreateStrategy(CreateService):
    async def create(self, db: AsyncSession, new_customer: ManagerSchema):
        customer_repo = DefaultCreateStrategy(db)
        return customer_repo.create(new_customer)

class ValidatedCreateStrategy(CreateService):
    async def create(self, db: AsyncSession, new_customer: ManagerSchema):
        AsyncSession