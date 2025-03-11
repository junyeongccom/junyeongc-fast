from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.staff.manager.service.update_service import UpdateService

class FullUpdateRepository(UpdateService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass

class PartialUpdateRepository(UpdateService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass