from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema

class CreateService(ABC):

    @abstractmethod
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        pass
