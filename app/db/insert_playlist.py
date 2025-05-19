import json

from deep_translator import GoogleTranslator
from pymilvus import Collection
from pymilvus import connections
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# 전역 모델 변수 (지연 로딩)
embedding_model = None
emotion_classifier = None

# 감정 매핑 테이블
emotion_map = {
    "joy": "기쁨", "sadness": "슬픔", "anger": "분노", "fear": "불안", "disgust": "혐오",
    "surprise": "놀람", "neutral": "중립"
}


def load_models():
    """모델을 처음 한 번만 로드"""
    global embedding_model, emotion_classifier
    if embedding_model is None:
        embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
    if emotion_classifier is None:
        emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            tokenizer="j-hartmann/emotion-english-distilroberta-base",
            top_k=1
        )


def truncate_text(text, max_chars=512):
    return text[:max_chars]


def classify_emotion(text: str) -> str:
    try:
        load_models()
        translated = GoogleTranslator(source="ko", target="en").translate(text)
        result = emotion_classifier(translated)
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
    load_models()
    insert_data = [[] for _ in range(12)]

    for item in playlist_data:
        try:
            combined_text = truncate_text(f"{item['description']} {item['track_summary']}")
            vector = embedding_model.encode(combined_text, normalize_embeddings=True)

            emotion_input = truncate_text(item.get("description", ""))
            emotion = classify_emotion(emotion_input)

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
    try:
        connections.connect("default", host="milvus", port="19530")
        collection = Collection("spotify_playlists")
        collection.load()
    except Exception as e:
        print(f"❌ Milvus 연결 또는 컬렉션 로딩 실패: {e}")
        return

    if any(len(col) == 0 for col in insert_data):
        print("❌ insert_data에 하나 이상의 비어 있는 필드가 있습니다. 삽입 중단.")
        return

    try:
        collection.insert(insert_data)
        print("\n✅ Milvus에 모든 데이터가 삽입되었습니다.")
    except Exception as e:
        print(f"\n❌ Milvus 삽입 중 오류 발생: {e}")


# CI 전용 main
if __name__ == "__main__":
    try:
        with open("data/cleaned_playlists.json", encoding="utf-8") as f:
            playlist_data = json.load(f)
        insert_data = prepare_insert_data(playlist_data)
        insert_to_milvus(insert_data)
    except FileNotFoundError:
        print("❌ 'data/cleaned_playlists.json' 파일을 찾을 수 없습니다.")