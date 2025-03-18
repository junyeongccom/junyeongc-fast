from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService


class SoftDeleteRepository(AbstractService):
    async def delete(self, db: AsyncSession, user_id: str):
        pass
        
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.delete(db, user_id)


class HardDeleteRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.delete(db, user_id)
        
    async def delete(self, db: AsyncSession, user_id: str):
        try:
            # Raw SQL 쿼리를 사용하여 회원 삭제
            query = f"DELETE FROM members WHERE user_id = '{user_id}'"
            print("🎉🎉 실행할 쿼리:", query)
            
            # 쿼리 실행 (commit 호출 제거)
            await db.execute(query)
            # commit 호출 제거 - 사용 중인 데이터베이스 연결 방식에서는 지원하지 않음
            
            # 삭제 결과 반환
            return {"status": "success", "message": f"회원 ID {user_id}가 성공적으로 삭제되었습니다."}
        except Exception as e:
            # 오류 메시지만 반환
            print("⚠️ 삭제 중 오류 발생:", str(e))
            return {"status": "error", "message": f"회원 삭제 중 오류 발생: {str(e)}"}
