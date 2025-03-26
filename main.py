from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from com.hc_fast.app_router import router as app_router
from com.hc_fast.utils.creational.builder.db_builder import get_db
from com.hc_fast.utils.creational.singleton.db_singleton import db_singleton

from dotenv import load_dotenv
import os

# ✅ .env 로드 (명시적 경로로)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"✅ main.py에서 .env 로드: {dotenv_path}")
load_dotenv(dotenv_path, override=True)

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
