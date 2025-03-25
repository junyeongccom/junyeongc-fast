# Async Database Builder
import os
import asyncpg
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from com.junyeongc.utils.creational.builder.query_builder import QueryBuilder
from com.junyeongc.utils.creational.singleton.db_singleton import db_singleton
import traceback


class DatabaseBuilder:
    def __init__(self):
        if not hasattr(db_singleton, "db_url"):
            raise AttributeError("⚠️ db_singleton 인스턴스에 'db_url' 속성이 존재하지 않습니다.")
        
        print(f"✅ Initializing DatabaseBuilder... db_url: {db_singleton.db_url}")

        self.database_url = db_singleton.db_url
        self.engine = None
        self.async_session = None

    async def build(self):
        if not self.database_url:
            raise ValueError("⚠️ Database URL must be set before building the database")

        print(f"🚀 Connecting to PostgreSQL: {self.database_url}")

        # SQLAlchemy async engine 생성
        self.engine = create_async_engine(
            self.database_url,
            echo=True,  # SQL 로그 출력
            pool_size=5,
            max_overflow=10
        )

        # AsyncSession 생성
        async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        return AsyncDatabase(self.engine, async_session)


class AsyncDatabase:
    def __init__(self, engine, async_session):
        self.engine = engine
        self.async_session = async_session

    async def fetch(self, query, *args):
        try:
            print(f"🔍 실행할 쿼리: {query}")
            print(f"🔢 쿼리 매개변수: {args}")
            
            async with self.async_session() as session:
                # 쿼리가 문자열인 경우 text() 함수로 감싸기
                if isinstance(query, str):
                    print("💬 문자열 쿼리를 SQLAlchemy text() 객체로 변환합니다.")
                    query = text(query)
                
                result = await session.execute(query, args)
                rows = result.fetchall()
                print(f"✅ 쿼리 실행 결과: {len(rows)}개의 행 반환됨")
                return rows
        except Exception as e:
            print(f"❌ 쿼리 실행 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise

    async def execute(self, query, *args):
        try:
            print(f"🔨 실행할 쿼리: {query}")
            print(f"🔢 쿼리 매개변수: {args}")
            
            async with self.async_session() as session:
                # 쿼리가 문자열인 경우 text() 함수로 감싸기
                if isinstance(query, str):
                    print("💬 문자열 쿼리를 SQLAlchemy text() 객체로 변환합니다.")
                    query = text(query)
                
                result = await session.execute(query, args)
                await session.commit()
                print("✅ 쿼리가 성공적으로 실행되고 커밋되었습니다.")
                return result
        except Exception as e:
            print(f"❌ 쿼리 실행 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise

    async def close(self):
        await self.engine.dispose()


# ✅ 3. FastAPI와 연동을 위한 Database Session Generator
# def get_db():
#     """SQLAlchemy 세션을 제공하는 FastAPI 종속성"""
#     db = session_local()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db():
    if not hasattr(db_singleton, "db_url") or not db_singleton.db_url:
        raise AttributeError("❌ db_singleton이 올바르게 초기화되지 않았습니다.")

    print(f"✅ db_singleton 초기화 확인: {db_singleton.db_url}")

    builder = DatabaseBuilder()
    db = await builder.build()

    try:
        yield db
    finally:
        await db.close()


# ✅ 4. 초기화 함수 (비동기 DB 테이블 생성)
async def init_db():
    """데이터베이스 초기화"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise e


# ✅ 5. 사용 예시
if __name__ == "__main__":
    # 🔹 SQLAlchemy DB 설정 빌드
    db_builder = (
        DatabaseBuilder()
        .echo(True)
        .future(True)
        .build()
    )

    engine = db_builder._engine
    session_local = db_builder._session_local
    Base = db_builder._base

    # 🔹 pymysql 쿼리 실행 예시
    query_result = (
        QueryBuilder()
        .connect()
        .query("SELECT * FROM users")
        .execute()
    )
    
    print(f"Query Result: {query_result}")