from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class DeleteService(ABC):

    @abstractmethod
    async def delete(self, db: AsyncSession, user_id: str):
        pass

    
