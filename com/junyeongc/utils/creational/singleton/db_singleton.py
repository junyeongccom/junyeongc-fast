import os
from threading import Lock
from dotenv import load_dotenv


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
load_dotenv(os.path.join(project_root, ".env"))


class DatabaseSingleton:
    _instance = None
    _lock = Lock()


    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    print("✅ DatabaseSingleton: Creating new instance")
                    cls._instance._initialize()
        return cls._instance


    def _initialize(self):
        print("✅ DatabaseSingleton: Running _initialize()")


        is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'




        self.db_hostname = os.getenv("DB_HOSTNAME")
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_database = os.getenv("DB_DATABASE")
        self.db_charset = os.getenv("DB_CHARSET")


        if is_docker:
            # Docker 컨테이너 내부에서 호스트 시스템에 접근하기 위해 host.docker.internal 사용
            self.db_hostname = "host.docker.internal"
        else:
            self.db_hostname = os.getenv("DB_HOSTNAME") or "localhost"




        print(f"🔹 Loaded Config - DB_HOSTNAME: {self.db_hostname}, DB_USERNAME: {self.db_username}, DB_DATABASE: {self.db_database}")




        # ✅ 환경 변수 검증
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            raise ValueError("⚠️ Database 환경 변수가 설정되지 않았습니다.")
        # ✅ PostgreSQL에 맞는 URL 형식
        self.db_url = f"postgresql://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"


        print(f"🛠️ Database URL: {self.db_url}")  # DSN 출력
        print(f"🛠️ DB Hostname: {self.db_hostname}")  # 호스트네임 출력






# ✅ 싱글톤 인스턴스를 생성하여 FastAPI 실행 시 자동으로 로드됨
db_singleton = DatabaseSingleton()
print("❗❗❗", db_singleton.db_url)
