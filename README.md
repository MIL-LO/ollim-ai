# 🎵 Ollim AI - Spotify 기반 감정 음악 추천 시스템

Ollim AI는 사용자의 감정을 바탕으로 Spotify API에서 플레이리스트 데이터를 수집하고,
이를 Milvus 벡터 데이터베이스에 임베딩하여 가장 적절한 음악을 추천하는 시스템입니다.

---

## 🧩 주요 기능

| 기능                         | 설명                                                                 |
|------------------------------|----------------------------------------------------------------------|
| 키워드 기반 플레이리스트 수집 | 감정 또는 분위기 키워드를 기반으로 Spotify에서 플레이리스트 최대 100개 수집 |
| 세부 정보 정제               | 각 플레이리스트의 설명, 이미지, 트랙 요약 정보를 정리해 JSON으로 저장     |
| Milvus 벡터 임베딩         | 정제된 JSON 데이터를 벡터화 후 Milvus에 저장                          |
| 감정 기반 추천             | 입력된 텍스트의 감정을 분석하고, 가장 적합한 음악 추천                 |
| 기능 테스트 자동화         | GitHub Actions 기반 유닛 테스트 CI 구축                                |

---

## 🗂️ 프로젝트 구조

```
ollim-ai/
├── app/
│   ├── api/                      # FastAPI 엔드포인트 (추천, 관리자용 수집 API 포함)
│   ├── db/                       # Milvus 스키마 정의 및 데이터 삽입 로직
│   ├── services/                # Spotify 연동, 임베딩, 추천 로직
│   └── tests/                   # 유닛 테스트 코드
├── data/                         # 수집된 JSON 파일 저장 경로
├── docker/                       # Milvus + MinIO + etcd 환경 구성
├── .github/workflows/ci.yml     # GitHub Actions CI 설정
├── .env                          # Spotify API 환경 변수 파일
├── requirements.txt              # Python 패키지 의존성 목록
└── README.md                     # 프로젝트 설명
```

---

## 🚀 실행 방법

### 1. 환경 변수 설정

`.env` 파일에 다음 내용을 추가하세요:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

또는 GitHub CI를 사용하는 경우 base64 인코딩 후 `ENV_BASE64`로 등록합니다.

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Milvus 서버 실행

```bash
cd docker
docker compose up -d
```

### 4. 추천 API 테스트

FastAPI Swagger UI에서 확인: [http://localhost:8001/docs](http://localhost:8001/docs)

```http
POST /recommend
{
  "user_id": "user1",
  "diary_id": "note123",
  "content": "오늘 하루 종일 마음이 무거웠고, 감정이 울적했어요.",
  "persona": {
    "mbti": "INFP",
    "age_group": "20s",
    "lifestyle": "student"
  }
}
```

### 5. 관리자 API를 통한 수집 및 삽입

```http
GET /admin/fetch-and-insert?keywords=슬픔&keywords=기쁨&keywords=사랑&limit=100
```

---

## 🧪 테스트 자동화

GitHub Actions는 PR 생성 시 다음을 자동 수행합니다:

1. `.env` 파일 생성 (Secrets 활용)
2. 패키지 설치
3. 유닛 테스트 수행

---

## 📌 참고 사항

- Milvus가 실행 중이어야 API 서버가 정상 작동합니다.
- 기본 벡터 모델: `intfloat/multilingual-e5-base`
- 감정 분석 모델: `j-hartmann/emotion-english-distilroberta-base`
