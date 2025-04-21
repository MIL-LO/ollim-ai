from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base")

def get_diary_embedding(content: str, persona: dict) -> list[float]:
    input_text = f"{persona['mbti']} {persona['age_group']} {persona['lifestyle']} {content}"
    return model.encode(input_text, normalize_embeddings=True).tolist()