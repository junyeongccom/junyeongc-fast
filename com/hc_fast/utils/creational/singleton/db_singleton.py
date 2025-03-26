import os
from threading import Lock

from dotenv import load_dotenv


# ✅ 단순화된 환경 변수 로드
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
        # 우선 DATABASE_URL 환경 변수 확인
        direct_url = os.getenv("DATABASE_URL")
        if direct_url:
            print(f"✅ DATABASE_URL 환경 변수를 사용합니다: {direct_url[:20]}...")
            
            # postgres:// 프로토콜이면 postgresql+asyncpg://로 변경
            if direct_url.startswith('postgres://'):
                self.db_url = direct_url.replace('postgres://', 'postgresql+asyncpg://', 1)
                print("✅ URL 프로토콜을 postgresql+asyncpg://로 변경했습니다.")
            # postgresql:// 프로토콜이면 postgresql+asyncpg://로 변경
            elif direct_url.startswith('postgresql://'):
                self.db_url = direct_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
                print("✅ URL에 asyncpg 드라이버를 추가했습니다.")
            else:
                # 이미 올바른 형식이거나 다른 형식인 경우
                self.db_url = direct_url
            
            return
        
        # 개별 환경 변수로부터 URL 구성
        self.db_hostname = os.getenv("DB_HOSTNAME")
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = int(os.getenv("DB_PORT", 5432))  # PostgreSQL 기본 포트는 5432
        self.db_database = os.getenv("DB_DATABASE")
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")


         # ✅ 환경 변수 검증
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            raise ValueError("⚠️ Database 환경 변수가 설정되지 않았습니다.")

        # ✅ PostgreSQL+asyncpg에 맞는 URL 형식 (비동기 드라이버 추가)
        self.db_url = f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        print(f"✅ 환경 변수로부터 PostgreSQL 연결 URL을 구성했습니다.")



# ✅ 싱글톤 인스턴스 생성
db_singleton = DataBaseSingleton()

# 테스트 환경에서는 전체 URL 출력 (디버깅 용이)
print("💯 db_singleton.db_url ▶️", db_singleton.db_url)