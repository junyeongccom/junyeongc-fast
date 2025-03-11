from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.service.delete_service import DeleteService


class SoftDeleteStrategy(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass


class HardDeleteStrategy(DeleteService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass
