from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class FullUpdate(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        # 모든 로직을 handle 메서드로 통합
        user_id = kwargs.get('user_id')
        customer_data = kwargs.get('customer_data')
        print(f"🔍 전체 업데이트 요청: {user_id}, 데이터: {customer_data}")
        # 여기에 전체 업데이트 로직 구현
        return {"status": "success", "message": f"회원 {user_id} 정보가 전체 업데이트되었습니다."}

class PartialUpdate(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        # 모든 로직을 handle 메서드로 통합
        user_id = kwargs.get('user_id')
        update_data = kwargs.get('update_data')
        print(f"🔍 부분 업데이트 요청: {user_id}, 데이터: {update_data}")
        # 여기에 부분 업데이트 로직 구현
        return {"status": "success", "message": f"회원 {user_id} 정보가 부분 업데이트되었습니다."}