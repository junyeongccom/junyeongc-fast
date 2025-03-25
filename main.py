from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from com.junyeongc.app_router import router as app_router 
import logging
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 미들웨어를 가장 먼저 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 도메인 허용 (필요시 특정 도메인으로 제한)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 추가
app.include_router(app_router, prefix="/api")

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

# 시작 시 환경 정보 로깅
@app.on_event("startup")
async def startup_event():
    logger.info("======== 서버 시작 ========")
    logger.info(f"환경: {os.environ.get('ENVIRONMENT', '개발')}")
    logger.info(f"데이터베이스 URL: {'설정됨 (보안상 내용 표시 안함)' if os.environ.get('DATABASE_URL') else '로컬 설정 사용'}")
    logger.info("==========================")


