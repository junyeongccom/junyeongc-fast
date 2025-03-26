from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from com.hc_fast.app_router import router as app_router
from com.hc_fast.utils.creational.builder.db_builder import get_db
from com.hc_fast.utils.creational.singleton.db_singleton import db_singleton

from dotenv import load_dotenv
import os

# 여러 방법으로 .env 파일 경로 시도
possible_paths = [
    # 1. 프로젝트 루트 디렉토리 (일반적인 상황)
    os.path.join(os.path.dirname(__file__), '.env'),
    # 2. 현재 작업 디렉토리
    os.path.join(os.getcwd(), '.env'),
    # 3. Docker 컨테이너 내부 경로
    '/app/.env'
]

env_file_found = False
for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ main.py: .env 파일을 찾았습니다: {path}")
        load_dotenv(path, override=True)
        env_file_found = True
        break

if not env_file_found:
    print("⚠️ main.py: .env 파일을 찾지 못했습니다. 환경 변수가 이미 설정되어 있는지 확인합니다.")

# ✅ FastAPI 앱 초기화
app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(app_router, prefix="/api")

# ✅ 루트 경로
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h1>🚀 FastAPI 테스트 서버 실행 중!</h1>
        </body>
    </html>
    """

# ✅ DB 연결 테스트용 엔드포인트
@app.get("/health/db")
async def test_db_connection(db=Depends(get_db)):
    result = await db.fetch("SELECT 1;")
    return {"db_check": result}


print(f"💯 main.py에서 직접 확인: db_singleton.db_url ▶ {db_singleton.db_url}")
