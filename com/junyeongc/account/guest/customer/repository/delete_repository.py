from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.service.delete_service import DeleteService


class SoftDeleteRepository(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass


class HardDeleteRepository(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass
