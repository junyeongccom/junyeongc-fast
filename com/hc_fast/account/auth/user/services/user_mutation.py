from com.hc_fast.account.auth.user.model.user_schema import UserSchema
from com.hc_fast.account.auth.user.repository.mutate_user import create_new_user
from com.hc_fast.utils.creational.abstract.abstract_service import AbstractService
from sqlalchemy.ext.asyncio import AsyncSession

class CreateNewUser(AbstractService):

    async def handle(self, **kwargs):
        db: AsyncSession = kwargs.get("db")
        new_user: UserSchema = kwargs.get("new_user")
        try:
            user = await create_new_user(new_user)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except Exception as e:
            print(f"[ERROR] UserCreate failed: {e}")
            await db.rollback()
            raise e