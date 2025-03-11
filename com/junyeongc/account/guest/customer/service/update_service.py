from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema


class UpdateService(ABC):

    @abstractmethod
    async def update(self, db: AsyncSession, update_customer: CustomerSchema):
        pass
