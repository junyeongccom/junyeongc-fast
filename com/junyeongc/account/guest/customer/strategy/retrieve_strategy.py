from com.junyeongc.account.guest.customer.service.retrieve_service import RetrieveService
from sqlalchemy.ext.asyncio import AsyncSession

class GetAllStrategy(RetrieveService):
    async def retrieve(self, db: AsyncSession, **kwargs):
        pass

class GetDetailStrategy(RetrieveService):
    async def retrieve(self, db: AsyncSession, user_id: str):
        pass
