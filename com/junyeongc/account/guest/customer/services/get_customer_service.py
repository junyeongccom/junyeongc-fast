from com.junyeongc.account.guest.customer.storage.get_customer import GetAllRepository, GetDetailRepository
from sqlalchemy.ext.asyncio import AsyncSession

from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class GetAll(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        return await self.retrieve(db, **kwargs)
        
    async def retrieve(self, db: AsyncSession, **kwargs):
        repository = GetAllRepository()
        return await repository.retrieve(db, **kwargs)

class GetDetail(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.retrieve(db, user_id)
        
    async def retrieve(self, db: AsyncSession, user_id: str):
        pass
