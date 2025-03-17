from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService


class DeleteCustomer(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.delete(db, user_id)
        
    async def delete(self, db: AsyncSession, user_id: str):
        pass


class RemoveCustomer(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.delete(db, user_id)
        
    async def delete(self, db: AsyncSession, user_id: str):
        pass
