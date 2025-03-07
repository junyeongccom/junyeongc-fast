from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from com.junyeongc.design_pattern.creational.singleton.db_singleton import db_singleton

# ✅ PostgreSQL 비동기 엔진 설정
engine = create_async_engine(db_singleton.db_url, echo=True)

# ✅ Base 객체 정의 (이 부분이 추가됨)
Base = declarative_base()

# ✅ 비동기 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ✅ 비동기 DB 세션 의존성 주입 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
