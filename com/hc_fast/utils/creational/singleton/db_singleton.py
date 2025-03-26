import os
from threading import Lock
from dotenv import load_dotenv

# ✅ 명시적인 .env 파일 경로 지정
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../../.env')
print(f"✅ 탐색할 .env 파일 경로: {dotenv_path}")
print(f"✅ 해당 파일 존재 여부: {os.path.exists(dotenv_path)}")

# ✅ 명시적 경로로 환경 변수 로드
load_dotenv(dotenv_path)

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
        # 환경 변수 디버깅을 위한 출력
        print("✅ 환경 변수 디버깅:")
        print("DB_HOSTNAME:", os.getenv("DB_HOSTNAME"))
        print("DB_USERNAME:", os.getenv("DB_USERNAME"))
        print("DB_PASSWORD:", os.getenv("DB_PASSWORD", "******"))  # 보안상 실제 값은 표시하지 않음
        print("DB_PORT:", os.getenv("DB_PORT"))
        print("DB_DATABASE:", os.getenv("DB_DATABASE"))
        print("DB_CHARSET:", os.getenv("DB_CHARSET"))
        print("DATABASE_URL:", os.getenv("DATABASE_URL", "Not Set"))
        
        # 우선 DATABASE_URL 환경 변수 확인
        direct_url = os.getenv("DATABASE_URL")
        if direct_url:
            print("✅ DATABASE_URL 환경 변수를 사용합니다.")
            
            # asyncpg는 'postgresql://' 형식을 사용
            self.db_url = direct_url
                
            print(f"✅ 사용할 DB URL: {self.db_url}")
            return
        
        # 개별 환경 변수에서 URL 구성
        self.db_hostname = os.getenv("DB_HOSTNAME")
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_database = os.getenv("DB_DATABASE")
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")

        # ✅ 환경 변수 검증
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            print("⚠️ 일부 환경 변수가 설정되지 않았습니다. 기본값을 사용합니다.")
            
            # 기본값 설정
            self.db_hostname = self.db_hostname or "database"
            self.db_username = self.db_username or "postgres"
            self.db_password = self.db_password or "mypassword"
            self.db_database = self.db_database or "my_database"
        
        # ✅ asyncpg용 URL 형식 (postgresql://)
        self.db_url = f"postgresql://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        print(f"✅ 환경 변수에서 구성된 DB URL: {self.db_url}")


# ✅ 싱글톤 인스턴스 생성
db_singleton = DataBaseSingleton()

print("💯 db_singleton.db_url ▶️", db_singleton.db_url)