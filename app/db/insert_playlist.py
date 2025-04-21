import json
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pymilvus import connections, Collection
from deep_translator import GoogleTranslator

# Milvus 연결
connections.connect("default", host="localhost", port="19530")
collection = Collection("spotify_playlists")
collection.load()

# 모델 로드
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    tokenizer="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

# 감정 라벨 매핑 (영어 → 한국어 or 사용자 지정)
emotion_map = {
    "joy": "기쁨",
    "sadness": "슬픔",
    "anger": "분노",
    "fear": "불안",
    "disgust": "혐오",
    "surprise": "놀람",
    "neutral": "중립"
}

def truncate_text(text, max_chars=512):
    """모델 입력 길이 초과 방지를 위한 문자열 자르기"""
    return text[:max_chars]

def classify_emotion(text: str) -> str:
    """감정 분석을 수행하고 감정 라벨을 반환"""
    try:
        translated = GoogleTranslator(source="ko", target="en").translate(text)
        result = emotion_classifier(translated)

        # top_k 사용 시 이중 리스트 대응
        if isinstance(result, list) and isinstance(result[0], list):
            result = result[0]
        if isinstance(result, list):
            result = result[0]

        label = result["label"].lower()
        return emotion_map.get(label, label)
    except Exception as e:
        print(f"[감정 분석 실패] 입력: {text} - {e}")
        return "분류불가"

def prepare_insert_data(playlist_data: list) -> list:
    """Milvus 삽입을 위한 insert_data 배열 구성"""
    insert_data = [[] for _ in range(12)]  # 총 12개 필드

    for item in playlist_data:
        try:
            # 텍스트 구성 및 벡터 임베딩
            combined_text = truncate_text(f"{item['description']} {item['track_summary']}")
            vector = embedding_model.encode(combined_text, normalize_embeddings=True)

            # 감정 분석 (description 기준)
            emotion_input = truncate_text(item.get("description", ""))
            emotion = classify_emotion(emotion_input)

            # 필드별 데이터 삽입
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

            print(f"삽입 준비 완료: {item['name']} ({emotion})")

        except Exception as e:
            print(f"삽입 실패: {item.get('name', 'UNKNOWN')} - {e}")

    return insert_data

def insert_to_milvus(insert_data: list):
    """Milvus에 데이터 삽입 수행"""
    if any(len(col) == 0 for col in insert_data):
        print("❌ insert_data에 하나 이상의 비어 있는 필드가 있습니다. 삽입 중단.")
        return

    try:
        collection.insert(insert_data)
        print("\n✅ Milvus에 모든 데이터가 삽입되었습니다.")
    except Exception as e:
        print(f"\n❌ Milvus 삽입 중 오류 발생: {e}")

def main():
    # JSON 로드
    with open("data/cleaned_playlists.json", "r", encoding="utf-8") as f:
        playlist_data = json.load(f)

    # 삽입 데이터 구성
    insert_data = prepare_insert_data(playlist_data)

    # Milvus에 삽입
    insert_to_milvus(insert_data)

if __name__ == "__main__":
    main()