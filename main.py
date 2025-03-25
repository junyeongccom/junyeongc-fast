from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from com.junyeongc.app_router import router as app_router 

app = FastAPI()
# CORS 미들웨어를 가장 먼저 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 임시로 모든 origin 허용
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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


