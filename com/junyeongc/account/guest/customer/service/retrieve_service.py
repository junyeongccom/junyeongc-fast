from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession



class RetrieveService(ABC):

    @abstractmethod
    async def retrieve(self, db: AsyncSession, **kwargs):
        pass

