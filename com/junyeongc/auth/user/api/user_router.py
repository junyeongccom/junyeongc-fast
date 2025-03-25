from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.common.user.model.user_schema import UserSchema
from com.junyeongc.auth.user.services.user_lookup import UserLookupService
from com.junyeongc.utils.creational.builder.db_builder import get_db

router = APIRouter()

@router.post("/login", response_model=UserSchema)
async def login(
    user_id: str = Body(...),
    password: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    print(f"로그인 요청 - ID: {user_id}, Password: {password}")  # 콘솔에 출력
    service = UserLookupService(db)
    return await service.login(user_id, password)

