from com.junyeongc.account.guest.customer.service.retrieve_service import RetrieveService
from sqlalchemy.ext.asyncio import AsyncSession

class GetAllRepository(RetrieveService):
    async def retrieve(self, db: AsyncSession, **kwargs):
        pass

class GetDetailRepository(RetrieveService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass