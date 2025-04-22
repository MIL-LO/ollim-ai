from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding import get_diary_embedding
from app.services.milvus_search import search_playlist

router = APIRouter()

# 사용자 프로필 정보 구조 정의
class Persona(BaseModel):
    mbti: str
    age_group: str
    lifestyle: str

# 추천 요청 구조 정의
class DiaryRequest(BaseModel):
    user_id: str
    diary_id: str
    content: str
    persona: Persona

# 추천 API: 사용자 입력 텍스트와 프로필 기반으로 유사한 플레이리스트 추천
@router.post("/recommend")
def recommend_playlist(request: DiaryRequest):
    # 1. 사용자 입력을 기반으로 임베딩 생성
    embedding = get_diary_embedding(request.content, request.persona.dict())

    # 2. Milvus에서 유사도 기반 추천 결과 조회 (top_k=5)
    results = search_playlist(embedding, top_k=5)

    # 3. 결과 리스트 생성
    response = []
    for hit in results:
        fields = hit.fields  # 또는 hit.entity (Milvus 버전에 따라)
        response.append({
            "id": str(fields.get("id", "")),
            "name": fields.get("name", ""),
            "description": fields.get("description", ""),
            "image_url": fields.get("image_url", ""),
            "image_width": int(fields.get("image_width", 0)),
            "image_height": int(fields.get("image_height", 0)),
            "owner_id": fields.get("owner_id", ""),
            "owner_name": fields.get("owner_name", ""),
            "followers": int(fields.get("followers", 0)),
            "track_summary": fields.get("track_summary", ""),
            "tag_emotion": fields.get("tag_emotion", ""),
            "similarity": round(1 - hit.distance, 4)  # cosine similarity 기반
        })

    return response