from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from com.junyeongc.app_router import router as app_router 

app = FastAPI()
# CORS 미들웨어를 가장 먼저 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 로컬 개발 서버
        "https://localhost:3000",  # HTTPS 로컬 개발 서버
        "https://haueull-chun-fast.onrender.com",  # 백엔드 배포 URL
    ],
    allow_credentials=True,  # 자격 증명 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


app.include_router(app_router, prefix="/api")


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


