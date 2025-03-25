from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.auth.user.api.user_controller import UserController
from com.junyeongc.account.auth.user.model.user_schema import UserLoginSchema, UserSchema
from com.junyeongc.utils.creational.builder.db_builder import get_db



router = APIRouter()
controller = UserController()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def handle_user(
    user_schema: UserLoginSchema = Body(...), 
    db: AsyncSession = Depends(get_db)):
    
    print("🔐 로그인 요청 받음")
    print(f"📝 요청된 아이디: {user_schema.user_id}")
    print(f"🔑 요청된 비밀번호: {user_schema.password}")
    print("📦 전체 요청 데이터:", user_schema.dict())

    result = await controller.login(user_schema=user_schema, db=db)
    print("🎯 로그인 처리 결과:", result)

    # 딕셔너리 응답을 직접 반환
    return JSONResponse(content=result)

