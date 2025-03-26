from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from com.hc_fast.app_router import router as app_router 
import logging
import os
import traceback
from contextlib import asynccontextmanager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행 코드
    logger.info("======== 서버 시작 1 ========")
    logger.info(f"환경: {os.environ.get('ENVIRONMENT', '개발')}")
    logger.info(f"데이터베이스 URL: {'설정됨 (보안상 내용 표시 안함)' if os.environ.get('DATABASE_URL') else '설정되지 않음'}")

    # 시스템 환경 변수 확인 (개발 환경에서만)
    if os.environ.get('ENVIRONMENT') != 'production':
        render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if render_hostname:
            logger.info(f"Render 호스트: {render_hostname}")
    
    logger.info("=============================")
    yield
    # 종료 시 실행 코드
    logger.info("======== 서버 종료 ========")

app = FastAPI(lifespan=lifespan)

# CORS 미들웨어를 가장 먼저 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 도메인 허용 (필요시 특정 도메인으로 제한)
    allow_credentials=False,  # 자격 증명 허용하지 않음 (쿠키 등 사용하지 않음)
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 추가
app.include_router(app_router, prefix="/api")

# 전역 예외 처리기
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 오류 로깅
    error_msg = f"전역 예외 발생: {str(exc)}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())
    
    # DNS 관련 오류 확인
    if "Name or service not known" in str(exc):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "데이터베이스 연결 중 DNS 해석 오류가 발생했습니다. 서버 관리자에게 문의하세요.",
                "detail": str(exc)
            }
        )
    
    # 일반적인 오류 응답
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "서버에서 처리 중 오류가 발생했습니다.",
            "detail": str(exc)
        }
    )

@app.get(path="/")
async def home():
    logger.info("루트 경로 접속됨")
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 현재 서버 구동 중입니다.</h1>
</div>
</body>
""")


