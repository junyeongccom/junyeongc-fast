from com.junyeongc.account.staff.manager.service.update_service import UpdateService
from sqlalchemy.ext.asyncio import AsyncSession


class FullUpdateStrategy(UpdateService):
    async def update(self, db: AsyncSession, user_id: str):
        pass

class PartialUpdateStrategy(UpdateService):
    async def update(self, db: AsyncSession, user_id: str):
        pass