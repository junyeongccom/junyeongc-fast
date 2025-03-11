from com.junyeongc.account.staff.manager.service.delete_service import DeleteService
from sqlalchemy.ext.asyncio import AsyncSession


class SoftDeleteStrategy(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass


class HardDeleteStrategy(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass