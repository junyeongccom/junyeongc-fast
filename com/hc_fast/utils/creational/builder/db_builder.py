# Async Database Builder
import os
import asyncpg
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from com.hc_fast.utils.creational.builder.query_builder import QueryBuilder
from com.hc_fast.utils.creational.singleton.db_singleton import db_singleton
import traceback
import logging

# 로거 설정
logger = logging.getLogger(__name__)

class DatabaseBuilder:
    def __init__(self):
        if not hasattr(db_singleton, "db_url"):
            raise AttributeError("⚠️ db_singleton 인스턴스에 'db_url' 속성이 존재하지 않습니다.")
        
        print(f"✅ Initializing DatabaseBuilder... db_url: {db_singleton.db_url}")

        self.database_url = db_singleton.db_url
        self.engine = None
        self.pool = None

    async def build(self):
        if not self.database_url:
            raise ValueError("⚠️ Database URL must be set before building the database")

        # 'database' 호스트 이름을 'localhost'로 변경 (Render.com 환경에서 필요)
        if "@database:" in self.database_url:
            old_url = self.database_url
            self.database_url = self.database_url.replace("@database:", "@localhost:")
            print(f"⚠️ 데이터베이스 URL의 호스트 이름을 변경합니다: database -> localhost")

        print(f"🚀 Connecting to PostgreSQL: {self.database_url}")

        try:
            # SQLAlchemy async engine 생성
            self.engine = create_async_engine(
                self.database_url,
                echo=True,  # SQL 로그 출력
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,  # 연결 확인
                pool_recycle=3600,   # 1시간마다 연결 재활용
            )

            # 연결 풀 생성
            self.pool = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False
            )

            return AsyncDatabase(self.pool)
        except Exception as e:
            print(f"❌ 데이터베이스 연결 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise


class AsyncDatabase:
    def __init__(self, pool):
        self.pool = pool

    async def fetch(self, query, *args):
        try:
            print(f"🔍 실행할 쿼리: {query}")
            print(f"🔢 쿼리 매개변수: {args}")
            
            # 연결 풀에서 세션 획득
            async with self.pool() as session:
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
            
            # 연결 풀에서 세션 획득
            async with self.pool() as session:
                try:
                    # 쿼리가 문자열인 경우 text() 함수로 감싸기
                    if isinstance(query, str):
                        print("💬 문자열 쿼리를 SQLAlchemy text() 객체로 변환합니다.")
                        query = text(query)
                    
                    result = await session.execute(query, args)
                    await session.commit()
                    print("✅ 쿼리가 성공적으로 실행되고 커밋되었습니다.")
                    return result
                except Exception as inner_e:
                    await session.rollback()
                    print(f"❌ 쿼리 실행 중 오류로 롤백합니다: {str(inner_e)}")
                    raise
        except Exception as e:
            print(f"❌ 쿼리 실행 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise

    async def close(self):
        if hasattr(self, 'engine') and self.engine:
            await self.engine.dispose()
        print("✅ 데이터베이스 연결이 정상적으로 종료되었습니다.")


# FastAPI와 연동을 위한 Database Session 의존성
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