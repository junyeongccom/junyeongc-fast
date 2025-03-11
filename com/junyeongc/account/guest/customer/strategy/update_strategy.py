from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.service.update_service import UpdateService

class FullUpdateStrategy(UpdateService):
    async def update(self, db: AsyncSession, user_id: str):
        pass

class PartialUpdateStrategy(UpdateService):
    async def update(self, db: AsyncSession, user_id: str):
        pass