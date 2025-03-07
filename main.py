from typing import List
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
import os
from fastapi import FastAPI
from com.junyeongc.design_pattern.creational.singleton.db_singleton import DatabaseSingleton
from database import get_db
from models import Member
from schemas import MemberSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


db_config = DatabaseSingleton()

print("💯🌈🚫🏁🌍▶️",db_config.db_hostname)
print("💯🌈🚫🏁🌍▶️",db_config.db_password)
print("💯🌈🚫🏁🌍▶️",db_config.db_port)
print("💯🌈🚫🏁🌍▶️",db_config.db_database)
print("💯🌈🚫🏁🌍▶️",db_config.db_charset)

# python -m uvicorn main:app --reload
# docker ps
# docker ps -a
# docker images
# docker start backend
# docker start database
# docker-compose
# docker exec -it postgres_container  psql -U postgres -d my_database
# docker exec -it backend bash
# docker compose logs fastapi
# docker compose logs --tail 10 fastapi
# docker-compose build --no-cache
# docker-compose up -d --force-recreate

app = FastAPI()


# current_time: Callable[[], str] = lambda: datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")


@app.get(path="/")
async def home():
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 현재 서버 구동 중입니다.</h1>

</div>
</body>
""")

#    <h2>{current_time()}</h2>


@app.get("/users", response_model=List[MemberSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    print("💻 get users로 진입 💻")

    # ✅ 비동기 ORM 쿼리 실행
    result = await db.execute(select(Member))
    users = result.scalars().all()

    return users