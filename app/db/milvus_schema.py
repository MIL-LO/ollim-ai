from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, connections

# Milvus 서버에 연결
connections.connect("default", host="localhost", port="19530")

# 필드 스키마 정의 (총 12개 필드)
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),  # playlist ID
    FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=300),                # playlist 이름
    FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1000),        # 설명
    FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=500),           # 썸네일 이미지
    FieldSchema(name="image_width", dtype=DataType.INT64),                           # 이미지 가로
    FieldSchema(name="image_height", dtype=DataType.INT64),                          # 이미지 세로
    FieldSchema(name="owner_id", dtype=DataType.VARCHAR, max_length=100),            # 작성자 ID
    FieldSchema(name="owner_name", dtype=DataType.VARCHAR, max_length=200),          # 작성자 이름
    FieldSchema(name="followers", dtype=DataType.INT64),                             # 팔로워 수
    FieldSchema(name="track_summary", dtype=DataType.VARCHAR, max_length=3000),      # 트랙 요약 정보 (벡터 임베딩용 텍스트)
    FieldSchema(name="tag_emotion", dtype=DataType.VARCHAR, max_length=50),          # 감정 태그
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768)                 # 벡터 임베딩
]

# 컬렉션 스키마 생성
schema = CollectionSchema(fields, description="Spotify Playlist Collection with emotion tags")

# 컬렉션 생성 (이미 있다면 생략됨)
collection = Collection(name="spotify_playlists", schema=schema)

# 벡터 필드에 인덱스 생성
collection.create_index(
    field_name="vector",
    index_params={
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
)

# 컬렉션 메모리에 로드
collection.load()

print("✅ 'spotify_playlists' 컬렉션이 생성 및 로드되었습니다.")