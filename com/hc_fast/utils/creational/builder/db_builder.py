import os
import asyncpg
import traceback
from dotenv import load_dotenv

from com.hc_fast.utils.creational.builder.query_builder import QueryBuilder
from com.hc_fast.utils.creational.singleton.db_singleton import db_singleton

# .env 파일 경로 명시적 지정
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../../.env')
print(f"✅ db_builder에서 탐색할 .env 파일 경로: {dotenv_path}")
print(f"✅ 해당 파일 존재 여부: {os.path.exists(dotenv_path)}")

# 명시적 경로로 환경 변수 로드
load_dotenv(dotenv_path)

# Async Database Builder
class DatabaseBuilder:
    def __init__(self):
        if not hasattr(db_singleton, "db_url"):
            raise AttributeError("⚠️ db_singleton 인스턴스에 'db_url' 속성이 존재하지 않습니다.")
        
        print(f"✅ Initializing DatabaseBuilder... db_url: {db_singleton.db_url}")

        self.database_url = db_singleton.db_url
        self.min_size = 1
        self.max_size = 10
        self.timeout = 60
        self.pool = None

    def pool_size(self, min_size: int = 1, max_size: int = 10):
        self.min_size = min_size
        self.max_size = max_size
        return self

    def timeout(self, timeout: int = 60):
        self.timeout = timeout
        return self

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
            # asyncpg 풀 생성 - 원래 방식으로 복원
            self.pool = await asyncpg.create_pool(
                dsn=self.database_url,
                min_size=self.min_size,
                max_size=self.max_size,
                timeout=self.timeout,
                command_timeout=self.timeout,
                server_settings={
                    'application_name': 'junyeongc_app'
                }
            )
            return AsyncDatabase(self.pool)
        except Exception as e:
            print(f"❌ 데이터베이스 연결 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise


class AsyncDatabase:
    def __init__(self, pool):
        self.pool = pool

    async def fetch(self, query: str, *args):
        try:
            print(f"🔍 실행할 쿼리: {query}")
            print(f"🔢 쿼리 매개변수: {args}")
            
            async with self.pool.acquire() as connection:
                result = await connection.fetch(query, *args)
                print(f"✅ 쿼리 실행 결과: {len(result)}개의 행 반환됨")
                return result
        except Exception as e:
            print(f"❌ 쿼리 실행 중 오류 발생: {str(e)}")
            traceback.print_exc()
            raise

    async def execute(self, query: str, *args):
        try:
            print(f"🔨 실행할 쿼리: {query}")
            print(f"🔢 쿼리 매개변수: {args}")
            
            async with self.pool.acquire() as connection:
                try:
                    result = await connection.execute(query, *args)
                    print("✅ 쿼리가 성공적으로 실행되었습니다.")
                    return result
                except Exception as inner_e:
                    print(f"❌ 쿼리 실행 중 오류 발생: {str(inner_e)}")
                    raise
        except Exception as e:
            print(f"❌ 데이터베이스 연결 오류: {str(e)}")
            traceback.print_exc()
            raise

    async def close(self):
        await self.pool.close()
        print("✅ 데이터베이스 연결 풀이 정상적으로 종료되었습니다.")


# FastAPI와 연동을 위한 Database Session 의존성
async def get_db():
    """데이터베이스 연결을 제공하는 FastAPI 의존성"""
    if not hasattr(db_singleton, "db_url") or not db_singleton.db_url:
        print("⚠️ db_singleton이 올바르게 초기화되지 않았습니다. 환경 변수를 다시 로드합니다.")
        
        # 환경 변수 재로드
        dotenv_path = os.path.join(os.path.dirname(__file__), '../../../../.env')
        print(f"✅ get_db에서 .env 파일 재로드: {dotenv_path}")
        load_dotenv(dotenv_path)
        
        # 환경 변수 출력
        print("DB_HOSTNAME:", os.getenv("DB_HOSTNAME"))
        print("DB_USERNAME:", os.getenv("DB_USERNAME"))
        print("DATABASE_URL:", os.getenv("DATABASE_URL"))
        
        # DATABASE_URL 환경 변수 확인
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            db_singleton.db_url = db_url
        else:
            # 개별 환경 변수로 URL 구성
            db_hostname = os.getenv("DB_HOSTNAME", "database")
            db_username = os.getenv("DB_USERNAME", "postgres")
            db_password = os.getenv("DB_PASSWORD", "mypassword")
            db_port = int(os.getenv("DB_PORT", 5432))
            db_database = os.getenv("DB_DATABASE", "my_database")
            
            db_singleton.db_url = f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}"
        
        print(f"✅ 재설정된 db_url: {db_singleton.db_url}")
        
        if not db_singleton.db_url:
            raise AttributeError("❌ 환경 변수를 다시 로드했지만 'db_url'이 설정되지 않았습니다. .env 파일을 확인하세요.")

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