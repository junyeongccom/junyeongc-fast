from com.junyeongc.account.guest.customer.storage.get_customer import GetAllRepository, GetDetailRepository
from sqlalchemy.ext.asyncio import AsyncSession

from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class GetAll(AbstractService):
    async def handle(self, **kwargs):
        repository = GetAllRepository()
        return await repository.retrieve(**kwargs)

class GetDetail(AbstractService):
    async def handle(self, **kwargs):
        repository = GetDetailRepository()
        return await repository.retrieve(**kwargs)
