from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService

class GetAllRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        return await self.retrieve(db, **kwargs)
        
    async def retrieve(self, db: AsyncSession, **kwargs):
        print("🎉🎉 GetAllRepository.retrieve 메서드 실행")
        query = "SELECT * FROM members"  

        try:
            # asyncpg 라이브러리 사용 (db는 asyncpg Connection 객체)
            rows = await db.fetch(query)
            print("💯🌈 조회된 행 수:", len(rows) if rows else 0)
            
            if rows:
                # asyncpg의 Record 객체를 딕셔너리로 변환
                customers = [dict(row) for row in rows]
                print("💯🌈 변환된 고객 데이터:", customers)
                return {"customers": customers}
            else:
                # 결과가 없는 경우
                print("⚠️ 조회된 데이터가 없습니다.")
                return {"customers": []}
                
        except Exception as e:
            print("⚠️ 데이터 조회 중 오류 발생:", str(e))
            import traceback
            traceback.print_exc()
            return {"error": f"데이터 조회 중 오류가 발생했습니다: {str(e)}"}

class GetDetailRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.retrieve(db, user_id)
        
    async def retrieve(self, db: AsyncSession, user_id: str):
        pass