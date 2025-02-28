# Python 3.10 기반 이미지 사용
FROM python:3.10

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 전체 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
