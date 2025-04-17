import json
import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pymilvus import connections, Collection

# Milvus 연결
connections.connect("default", host="localhost", port="19530")
collection = Collection("spotify_playlists")
collection.load()

# 모델 로드
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

def truncate_text(text, max_chars=512):
    """모델 입력 길이 초과 방지를 위한 문자열 자르기"""
    return text[:max_chars]

# JSON 로드
with open("data/cleaned_playlists.json", "r", encoding="utf-8") as f:
    playlist_data = json.load(f)

# 삽입할 데이터 준비
insert_data = [[] for _ in range(12)]  # 총 12개 필드

for item in playlist_data:
    try:
        # 텍스트 구성 및 자르기
        combined_text = f"{item['name']} {item['description']} {item['track_summary']}"
        combined_text = truncate_text(combined_text)

        # 임베딩 및 감정 태그
        vector = embedding_model.encode(combined_text, normalize_embeddings=True)
        emotion = emotion_classifier(item['description'])[0]['label']

        # 데이터 필드별 삽입
        insert_data[0].append(item.get("id", ""))
        insert_data[1].append(item.get("name", ""))
        insert_data[2].append(item.get("description", ""))
        insert_data[3].append(item.get("image_url", ""))
        insert_data[4].append(int(item.get("image_width") or 0))
        insert_data[5].append(int(item.get("image_height") or 0))
        insert_data[6].append(item.get("owner_id", ""))
        insert_data[7].append(item.get("owner_name", ""))
        insert_data[8].append(int(item.get("followers") or 0))
        insert_data[9].append(item.get("track_summary", ""))
        insert_data[10].append(emotion)
        insert_data[11].append(vector.tolist())

        print(f"삽입 준비 완료: {item['name']}")

    except Exception as e:
        print(f"삽입 실패: {item.get('name')} - {e}")

# Milvus에 데이터 삽입
collection.insert(insert_data)
print("\nMilvus에 모든 데이터가 삽입되었습니다.")