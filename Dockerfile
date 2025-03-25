# Python 3.10 기반 이미지 사용
FROM python:3.10

# 필요한 시스템 도구 설치
RUN apt-get update && apt-get install -y \
    iputils-ping \
    dnsutils \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 전체 복사
COPY . .

# 환경 변수 설정
ENV ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1

# DNS 설정 확인 (빌드 시 진단용)
RUN echo "Checking DNS settings:" && cat /etc/resolv.conf

# FastAPI 실행 (개발 모드의 --reload 옵션 제거)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
