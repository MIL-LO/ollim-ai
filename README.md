# 🎵 Ollim AI - Spotify 기반 감정 음악 추천 시스템

Ollim AI는 사용자의 감정을 바탕으로 Spotify API에서 플레이리스트 데이터를 수집하고, 이를 Milvus 벡터 데이터베이스에 임베딩하여 가장 적절한 음악을 추천하는 시스템입니다.

---

## 🧩 주요 기능

| 기능                         | 설명                                                                 |
|------------------------------|----------------------------------------------------------------------|
| 🔍 키워드 기반 플레이리스트 수집 | 감정 또는 분위기 키워드를 기반으로 Spotify에서 플레이리스트 100개 수집 |
| 📑 세부 정보 정제               | 각 플레이리스트의 설명, 이미지, 트랙 요약 정보를 정리해 JSON으로 저장     |
| 📦 Milvus 벡터 임베딩         | 정제된 JSON 데이터를 벡터화 후 Milvus에 저장                          |
| 🤖 감정 기반 추천             | 입력된 텍스트의 감정을 분석하고, 가장 적합한 음악 추천                 |
| ✅ 기능 테스트 자동화         | GitHub Actions 기반 유닛 테스트 CI 구축                                |

---

## 🗂️ 프로젝트 구조

```
ollim-ai/
├── app/
│   ├── api/                      # Spotify API 클라이언트 정의
│   ├── db/                       # Milvus 스키마 생성 및 샘플 데이터 삽입
│   ├── services/                # 기능 로직 (데이터 수집, 감정 분석 등)
│   └── tests/                   # 유닛 테스트 코드
├── data/                         # 수집된 JSON 파일 저장
├── docker/                       # Milvus + MinIO + etcd용 docker-compose
├── .github/workflows/ci.yml     # GitHub Actions CI 설정
├── .env                          # Spotify API 키 등 환경 변수 파일
├── requirements.txt              # Python 의존성
└── README.md                     # 프로젝트 설명
```

---

## 🚀 실행 방법

### 1. 환경 변수 설정

`.env` 파일에 다음과 같은 내용을 작성하세요:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

또는 GitHub CI를 사용할 경우 base64 인코딩하여 `ENV_BASE64`로 저장하세요.

### 2. 의존성 설치

```bash
conda activate ollim-ai
pip install -r requirements.txt
```

### 3. Milvus 서버 실행

```bash
cd docker
docker compose up -d
```

### 4. 컬렉션 생성 및 데이터 삽입

```bash
python app/db/milvus_schema.py
python app/db/insert_sample_data.py
```

### 5. 음악 추천 테스트 실행

```bash
python app/tests/test_recommender.py
```

---

## 🧪 테스트 자동화

GitHub Actions는 Pull Request 시 다음을 자동 수행합니다:

1. `.env` 파일 생성 (Secrets 활용)
2. 패키지 설치
3. 기능 테스트 수행

워크플로우 파일: `.github/workflows/ci.yml`