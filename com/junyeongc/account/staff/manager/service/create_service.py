from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema

class CreateService(ABC):

    @abstractmethod
    async def create(self, db: AsyncSession, new_manager: CustomerSchema):
        pass