from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.auth.user.models.user_entity import UserEntity

class FindUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, user_id: str):
        """
        사용자 ID로 사용자를 조회합니다.
        """
        # SQLAlchemy Core 방식으로 쿼리 작성
        stmt = select(UserEntity).where(UserEntity.user_id == user_id)
        # execute를 사용하여 쿼리 실행
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()