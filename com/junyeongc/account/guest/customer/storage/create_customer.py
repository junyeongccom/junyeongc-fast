from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.models.customer_entity import CustomerEntity
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService



class DefaultCreateRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        new_customer = kwargs.get('customer_data')
        return await self.create(db, new_customer)
        
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        print("😃😃Repository new_customer:", new_customer)
        try:
            # asyncpg를 사용하여 직접 SQL 쿼리 실행
            query = """
                INSERT INTO members (user_id, name, email, password)
                VALUES ($1, $2, $3, $4)
            """
            
            # 쿼리 실행
            await db.execute(
                query,
                new_customer.user_id,
                new_customer.name,
                new_customer.email,
                new_customer.password
            )
            
            print("✅ 회원가입 성공:", new_customer.user_id)
            
            # 성공 응답 반환
            return {"status": "success", "message": "회원가입이 완료되었습니다.", "user_id": new_customer.user_id}
        except Exception as e:
            # 오류 발생 시 출력
            print("⚠️ 회원가입 중 오류 발생:", str(e))
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"회원가입 중 오류가 발생했습니다: {str(e)}"}
        
class ValidatedCreateRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        new_customer = kwargs.get('customer_data')
        return await self.create(db, new_customer)
        
    async def create(self, db: AsyncSession, new_customer: CustomerSchema):
        # 유효성 검사 로직 추가
        # 예: 이메일 형식 검사, 비밀번호 강도 검사 등
        
        # 검사 통과 후 기본 저장소로 위임
        default_repo = DefaultCreateRepository()
        return await default_repo.create(db, new_customer)