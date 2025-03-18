from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService
from com.junyeongc.account.guest.customer.storage.delete_customer import HardDeleteRepository


class DeleteCustomer(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        # 모든 로직을 handle 메서드로 통합
        user_id = kwargs.get('user_id')
        # 하드 삭제 리포지토리를 사용하여 회원 삭제
        repository = HardDeleteRepository()
        return await repository.delete(db, user_id)


class RemoveCustomer(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        # 모든 로직을 handle 메서드로 통합
        user_id = kwargs.get('user_id')
        # 소프트 삭제 로직 (향후 구현 가능)
        print(f"🔍 소프트 삭제 요청: {user_id}")
        return {"status": "success", "message": f"회원 {user_id}를 소프트 삭제했습니다."}
