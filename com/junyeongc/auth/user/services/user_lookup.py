from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.auth.user.repository.find_user import FindUserRepository
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLookupService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.find_user_repository = FindUserRepository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        평문 비밀번호와 해시된 비밀번호를 비교합니다.
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def login(self, user_id: str, password: str):
        """
        사용자 로그인을 처리합니다.
        """
        # 1. user_id로 먼저 조회
        user = await self.find_user_repository.find_by_id(user_id)
        
        # 일치하는 ID가 없으면 에러 반환
        if not user:
            raise HTTPException(status_code=401, detail="고객에서 등록된 ID가 없습니다")
            
        # 2. ID가 있으면, 해시된 비밀번호와 비교
        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다")
            
        return {
            "message": "로그인에 성공하였습니다",
            "user_id": user.user_id,
            "name": user.name
        }
