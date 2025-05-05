# FastAPI 기반 Python 컨테이너
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 기본 패키지 설치 (tini 포함 추천)
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 소스 복사
COPY . .

# 환경변수 설정
ENV PYTHONPATH=/app

# uvicorn 실행은 docker-compose에서 override 예정