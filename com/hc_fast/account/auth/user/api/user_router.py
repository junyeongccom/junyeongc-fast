from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from com.hc_fast.account.auth.user.api.user_controller import UserController
from com.hc_fast.account.auth.user.model.user_schema import UserLoginSchema, UserSchema
from com.hc_fast.utils.creational.builder.db_builder import get_db
import logging
import traceback

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter()
controller = UserController()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def handle_user(
    user_schema: UserLoginSchema = Body(...), 
    db: AsyncSession = Depends(get_db)):
    
    logger.info(f"🔐 로그인 요청 받음: 사용자 ID={user_schema.user_id}")
    
    try:
        # 로그인 처리
        result = await controller.login(user_schema=user_schema, db=db)
        
        if result.get("status") == "success":
            logger.info(f"🎯 로그인 성공: 사용자 ID={user_schema.user_id}")
        else:
            logger.warning(f"⚠️ 로그인 실패: 사용자 ID={user_schema.user_id}, 이유={result.get('message')}")
            
        # 결과 반환
        return JSONResponse(content=result)
        
    except Exception as e:
        error_msg = f"🔴 로그인 처리 중 예외 발생: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())  # 상세 스택 트레이스 로깅
        
        # 클라이언트에게 오류 응답
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"로그인 처리 중 서버 오류가 발생했습니다: {str(e)}",
                "user": None
            }
        )

