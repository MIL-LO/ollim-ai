from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from deep_translator import GoogleTranslator

# 연결 및 모델 준비
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", tokenizer="j-hartmann/emotion-english-distilroberta-base", top_k=1)

emotion_map = {
    "joy": "기쁨", "sadness": "슬픔", "anger": "분노", "fear": "불안", "disgust": "혐오",
    "surprise": "놀람", "neutral": "중립"
}

def truncate_text(text, max_chars=512):
    return text[:max_chars]

def classify_emotion(text: str) -> str:
    try:
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
    connections.connect("default", host="milvus", port="19530")
    collection = Collection("spotify_playlists")
    collection.load()

    if any(len(col) == 0 for col in insert_data):
        print("❌ insert_data에 하나 이상의 비어 있는 필드가 있습니다. 삽입 중단.")
        return

    try:
        collection.insert(insert_data)
        print("\n✅ Milvus에 모든 데이터가 삽입되었습니다.")
    except Exception as e:
        print(f"\n❌ Milvus 삽입 중 오류 발생: {e}")