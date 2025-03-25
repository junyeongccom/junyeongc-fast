# ✅ 단순화된 환경 변수 로드
import os
from threading import Lock
from dotenv import load_dotenv


load_dotenv()

class DataBaseSingleton:

    _instance = None
    _lock = Lock()  # :white_check_mark: 멀티스레드 환경에서도 안전하게 인스턴스를 생성하도록 락 사용

    def __new__(cls):
        """싱글톤 인스턴스 생성"""
        if not cls._instance:
            with cls._lock:  # :white_check_mark: 멀티스레드 환경에서 안전하게 인스턴스 생성
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """환경 변수 값을 로드하여 설정 초기화"""
        # Render.com에서 제공하는 DATABASE_URL이 있는지 먼저 확인
        database_url = os.getenv("DATABASE_URL")
        
        # DATABASE_URL이 있으면 이를 우선적으로 사용
        if database_url:
            print("✅ Render.com DATABASE_URL 환경 변수를 사용합니다.")
            self.db_url = database_url
            return
            
        # 개별 환경 변수 설정
        self.db_hostname = os.getenv("DB_HOSTNAME", "database")
        self.db_username = os.getenv("DB_USERNAME", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "mypassword")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_database = os.getenv("DB_DATABASE", "my_database")
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")

        # ✅ 환경 변수 검증
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            raise ValueError("⚠️ Database 환경 변수가 설정되지 않았습니다.")

        # ✅ PostgreSQL에 맞는 URL 형식 (asyncpg 드라이버 사용)
        self.db_url = f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        print("✅ 로컬 환경 변수를 사용하여 데이터베이스 URL을 구성합니다.")


# ✅ 싱글톤 인스턴스 생성
db_singleton = DataBaseSingleton()

print("💯 db_singleton.db_url ▶️",db_singleton.db_url)