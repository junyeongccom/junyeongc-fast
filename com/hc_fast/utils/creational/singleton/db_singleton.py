# ✅ 단순화된 환경 변수 로드
import os
from threading import Lock
from dotenv import load_dotenv
import re
import logging
import socket
import time

# 로거 설정
logger = logging.getLogger(__name__)

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
            logger.info("✅ DATABASE_URL 환경 변수를 사용합니다.")
            
            # Render의 DATABASE_URL은 postgres://user:password@host:port/dbname 형식일 수 있음
            # PostgreSQL+asyncpg는 postgresql+asyncpg://user:password@host:port/dbname 형식 필요
            if database_url.startswith('postgres://'):
                # postgres:// 프로토콜을 postgresql+asyncpg://로 변경
                database_url = database_url.replace('postgres://', 'postgresql+asyncpg://', 1)
                logger.info("✅ DATABASE_URL 프로토콜을 postgresql+asyncpg://로 변경했습니다.")
            
            # 이미 postgresql://로 시작하는 경우 asyncpg 드라이버 추가
            elif database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
                logger.info("✅ DATABASE_URL에 asyncpg 드라이버를 추가했습니다.")
            
            # 다른 형식의 URL인 경우 로그 남기기
            else:
                logger.warning(f"⚠️ 인식되지 않은 데이터베이스 URL 형식: {database_url[:10]}...")
            
            # 호스트 이름을 처리하는 부분
            try:
                # 호스트 추출 (user:password@host:port/dbname에서 host 부분)
                host_match = re.search(r'@([^:]+)(:|/)', database_url)
                if host_match:
                    host = host_match.group(1)
                    # IP 주소 형식이 아닌 경우 DNS 확인 시도
                    if not re.match(r'^\d+\.\d+\.\d+\.\d+$', host):
                        logger.info(f"ℹ️ 호스트 도메인 이름을 확인 중입니다: {host}")
                        try:
                            # DNS 조회를 위한 최대 3번의 시도
                            max_attempts = 3
                            for attempt in range(max_attempts):
                                try:
                                    ip_address = socket.gethostbyname(host)
                                    logger.info(f"✅ 호스트 {host}의 IP 주소 확인: {ip_address}")
                                    
                                    # URL에서 호스트 이름을 IP 주소로 교체
                                    database_url = database_url.replace(f"@{host}:", f"@{ip_address}:")
                                    logger.info(f"✅ URL의 호스트 이름을 IP 주소로 변경했습니다.")
                                    break
                                except socket.gaierror:
                                    if attempt < max_attempts - 1:
                                        wait_time = 2 ** attempt  # 지수 백오프 (1, 2, 4초)
                                        logger.warning(f"⚠️ 호스트 이름 해석 실패. {wait_time}초 후 재시도 ({attempt+1}/{max_attempts})...")
                                        time.sleep(wait_time)
                                    else:
                                        logger.error(f"❌ 호스트 이름 '{host}' 해석 실패. 원본 URL을 사용합니다.")
                        except Exception as dns_err:
                            logger.error(f"❌ DNS 조회 중 오류 발생: {str(dns_err)}")
            except Exception as e:
                logger.warning(f"⚠️ 호스트 이름 확인 중 오류: {str(e)}")
            
            self.db_url = database_url
            return
            
        # 개별 환경 변수 설정 (로컬 개발 환경)
        self.db_hostname = os.getenv("DB_HOSTNAME", "database")
        self.db_username = os.getenv("DB_USERNAME", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "mypassword")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_database = os.getenv("DB_DATABASE", "my_database")
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")

        # ✅ 환경 변수 검증
        if None in (self.db_hostname, self.db_username, self.db_password, self.db_database):
            raise ValueError("⚠️ Database 환경 변수가 설정되지 않았습니다.")

        # ✅ 호스트 이름이 도메인인 경우 IP 주소로 변환 시도
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', self.db_hostname):
            try:
                ip_address = socket.gethostbyname(self.db_hostname)
                logger.info(f"✅ 호스트 {self.db_hostname}의 IP 주소 확인: {ip_address}")
                self.db_hostname = ip_address
            except socket.gaierror:
                logger.warning(f"⚠️ 호스트 이름 '{self.db_hostname}'의 IP 주소를 확인할 수 없습니다. 원본 호스트 이름을 사용합니다.")
            except Exception as e:
                logger.warning(f"⚠️ IP 주소 변환 중 오류 발생: {str(e)}")

        # ✅ PostgreSQL에 맞는 URL 형식 (asyncpg 드라이버 사용)
        self.db_url = f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"
        logger.info("✅ 로컬 환경 변수를 사용하여 데이터베이스 URL을 구성합니다.")


# ✅ 싱글톤 인스턴스 생성
db_singleton = DataBaseSingleton()

# URL의 호스트 이름 부분을 마스킹하여 출력
masked_url = db_singleton.db_url
try:
    # 사용자 이름, 비밀번호, 호스트 이름을 마스킹
    masked_url = re.sub(r'(postgresql\+asyncpg://)[^@]+@([^/]+)/', r'\1***:***@\2/', db_singleton.db_url)
except Exception:
    masked_url = "마스킹 실패, URL 형식이 예상과 다릅니다."

logger.info(f"💯 DB 연결 URL: {masked_url}")
