from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService


class SoftDeleteRepository(AbstractService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass


class HardDeleteRepository(AbstractService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass
