import os
from threading import Lock
from dotenv import load_dotenv

# ✅ 단순화된 환경 변수 로드
load_dotenv()

class DataBaseSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """싱글톤 인스턴스 생성"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """환경 변수 값을 로드하여 설정 초기화"""
        self.db_hostname = os.getenv("DB_HOSTNAME")
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_database = os.getenv("DB_DATABASE")
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")
        
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            raise ValueError("⚠️ Database 환경 변수가 설정되지 않았습니다.")

        
        # ✅ asyncpg용 URL 형식 (postgresql://)
        self.db_url = f"postgresql://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        print(f"✅ 환경 변수에서 구성된 DB URL: {self.db_url}")

# ✅ 싱글톤 인스턴스 생성
db_singleton = DataBaseSingleton()

print("💯 db_singleton.db_url ▶️", db_singleton.db_url)