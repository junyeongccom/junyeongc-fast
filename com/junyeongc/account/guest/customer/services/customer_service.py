from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from com.junyeongc.account.guest.customer.models.customer_entity import CustomerEntity
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema

class CustomerService:
    @staticmethod
    async def create_customer(db: AsyncSession, customer: CustomerSchema) -> CustomerSchema:
        # 기존 사용자 확인
        stmt = select(CustomerEntity).where(CustomerEntity.user_id == customer.user_id)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 사용자 ID입니다."
            )
        
        # 새 사용자 생성
        db_customer = CustomerEntity(
            user_id=customer.user_id,
            password=customer.password,  # 평문 비밀번호 저장
            name=customer.name,
            email=customer.email
        )
        
        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        
        return CustomerSchema.model_validate(db_customer)

    @staticmethod
    async def login_customer(db: AsyncSession, user_id: str, password: str) -> dict:
        # 사용자 조회
        stmt = select(CustomerEntity).where(CustomerEntity.user_id == user_id)
        result = await db.execute(stmt)
        customer = result.scalar_one_or_none()
        
        # 사용자가 없는 경우
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        # 비밀번호 검증 (평문 비교)
        if password != customer.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="아이디 또는 비밀번호가 일치하지 않습니다."
            )
        
        # 로그인 성공 응답
        return {
            "status": "success",
            "message": "로그인 성공",
            "user": CustomerSchema.model_validate(customer).dict()
        } 