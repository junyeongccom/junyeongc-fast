import os
import asyncpg
import traceback
from dotenv import load_dotenv

from com.hc_fast.utils.creational.singleton.db_singleton import db_singleton

# 여러 방법으로 .env 파일 경로 시도
possible_paths = [
    # 1. 프로젝트 루트 디렉토리
    os.path.join(os.getcwd(), '.env'),
    # 2. 현재 파일의 상대 경로
    os.path.join(os.path.dirname(__file__), '../../../../.env'),
    # 3. Docker 컨테이너 내부 경로
    '/app/.env'
]

env_file_found = False
for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ db_builder.py: .env 파일을 찾았습니다: {path}")
        load_dotenv(path)
        env_file_found = True
        break

if not env_file_found:
    print("⚠️ db_builder.py: .env 파일을 찾지 못했습니다. 환경 변수가 이미 설정되어 있는지 확인합니다.")

# Async Database Builder - 코어 방식 (raw SQL, 순수 함수, 상태 없음)
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

    def set_timeout(self, timeout: int = 60):
        self.timeout = timeout
        return self

    async def build(self):
        if not self.database_url:
            raise ValueError("⚠️ Database URL must be set before building the database")

        print(f"🚀 Connecting to PostgreSQL: {self.database_url}")

        try:
            # asyncpg 풀 생성
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
        """Raw SQL 쿼리를 실행하고 여러 행의 결과를 반환합니다."""
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
        """Raw SQL 쿼리를 실행하고 영향을 받은、 행 수나 상태를 반환합니다."""
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
        """데이터베이스 연결 풀을 닫습니다."""
        await self.pool.close()
        print("✅ 데이터베이스 연결 풀이 정상적으로 종료되었습니다.")


# FastAPI와 연동을 위한 Database Session 의존성
async def get_db():
    """데이터베이스 연결을 제공하는 FastAPI 의존성"""
    if not hasattr(db_singleton, "db_url") or not db_singleton.db_url:
        print("⚠️ db_singleton이 올바르게 초기화되지 않았습니다. 환경 변수를 다시 로드합니다.")
        
        # 환경 변수 재로드
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ get_db()에서 .env 파일 재로드: {path}")
                load_dotenv(path)
                break
        
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


# 사용 예시 (코어 방식)
if __name__ == "__main__":
    import asyncio
    
    async def test_db_operations():
        # DB 연결 생성
        builder = DatabaseBuilder()
        db = await builder.build()
        
        try:
            # 테이블 생성 (생성되어 있다면 무시)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS test_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 데이터 삽입
            await db.execute(
                "INSERT INTO test_users (username, email) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                "testuser", "test@example.com"
            )
            
            # 데이터 조회
            users = await db.fetch("SELECT * FROM test_users")
            print(f"사용자 목록: {users}")
            
        finally:
            # 연결 종료
            await db.close()
    
    # 비동기 함수 실행
    asyncio.run(test_db_operations())