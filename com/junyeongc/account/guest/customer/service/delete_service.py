from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.model.customer_schema import CustomerSchema


class DeleteService(ABC):

    @abstractmethod
    async def delete(self, db: AsyncSession, user_id: str):
        pass

    
