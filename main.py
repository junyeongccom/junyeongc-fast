from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 환경 변수 직접 설정
os.environ["DB_HOSTNAME"] = "localhost"

from com.junyeongc import app_router
from com.junyeongc.utils.creational.singleton.db_singleton import DatabaseSingleton
from com.junyeongc.app_router import router as app_router 

db_config = DatabaseSingleton()

print("💯🌈🚫🏁🌍▶️",db_config.db_hostname)
print("💯🌈🚫🏁🌍▶️",db_config.db_password)
print("💯🌈🚫🏁🌍▶️",db_config.db_port)
print("💯🌈🚫🏁🌍▶️",db_config.db_database)
print("💯🌈🚫🏁🌍▶️",db_config.db_username)

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용 (개발 환경용, 프로덕션에서는 구체적인 오리진 지정)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(app_router)

@app.get(path="/")
async def home():
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 현재 서버 구동 중입니다.</h1>

</div>
</body>
""")
# current_time: Callable[[], str] = lambda: datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")
#    <h2>{current_time()}</h2>


