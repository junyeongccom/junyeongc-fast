
#from datetime import datetime
#from pytz import timezone
from typing import Callable
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from com.junyeongc.auth.climate.web.climate_router import router as climate_router
from com.junyeongc.auth.user.web.user_router import router as user_router
from com.junyeongc.auth.admin.web.admin_router import router as admin_router

# python -m uvicorn main:app --reload

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(climate_router, prefix="/admin", tags=["Admin"])

#current_time: Callable[[], str] = lambda: datetime.now(datetime.timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")
@app.get(path="/")
async def home():
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 현재 서버 구동 중입니다.</h1>
    
</div>
</body>
""")

#<h2>{current_time()}</h2>

@app.get("/")
def read_root():
    return {"main":"메인 라우터"}