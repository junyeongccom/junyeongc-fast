from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class FullUpdate(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.update(db, user_id)
        
    async def update(self, db: AsyncSession, user_id: str):
        pass

class PartialUpdate(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.update(db, user_id)
        
    async def update(self, db: AsyncSession, user_id: str):
        pass