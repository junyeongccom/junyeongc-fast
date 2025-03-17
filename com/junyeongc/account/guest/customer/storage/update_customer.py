from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class FullUpdateRepository(AbstractService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass

class PartialUpdateRepository(AbstractService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass