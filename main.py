from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
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


