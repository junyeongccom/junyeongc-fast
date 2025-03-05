
#from datetime import datetime
#from pytz import timezone
from sqlalchemy import select, text
from typing import Callable
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from com.junyeongc.auth.climate.web.climate_router import router as climate_router
from com.junyeongc.auth.user.web.user_router import router as user_router
from com.junyeongc.auth.admin.web.admin_router import router as admin_router
from com.junyeongc.auth.user.repository.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.auth.user.repository.database import engine
from models import Member

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

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """PostgreSQL의 members 테이블 데이터를 반환하는 API"""
    try:
        result = await db.execute(select(Member))  # ✅ members 테이블 조회
        members = result.scalars().all()  # ✅ 조회 결과 변환

        # JSON 형태로 변환
        members_list = [
            {"user_id": member.user_id, "email": member.email, "password": member.password, "name": member.name}
            for member in members
        ]
        
        return {"members": members_list}

    except Exception as e:
        return {"error": str(e)}

@app.get("/test-db")
async def test_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # ✅ SQLAlchemy의 text() 사용
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": str(e)}