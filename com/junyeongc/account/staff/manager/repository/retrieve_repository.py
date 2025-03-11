from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.staff.manager.service.retrieve_service import RetrieveService

class GetAllRepository(RetrieveService):
    async def retrieve(self, db: AsyncSession, **kwargs):
        pass

class GetDetailRepository(RetrieveService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass