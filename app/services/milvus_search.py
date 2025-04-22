from pymilvus import connections, Collection

def search_playlist(embedding: list[float], top_k=5):
    # Milvus 연결 (이미 연결되어 있다면 생략 가능)
    connections.connect(alias="default", host="localhost", port="19530")
    
    # 컬렉션 로드
    collection = Collection("spotify_playlists", using="default")
    collection.load()

    # 벡터 유사도 검색 수행
    results = collection.search(
        data=[embedding],                     # 검색 기준 벡터
        anns_field="vector",                  # 비교할 필드
        param={"metric_type": "COSINE", "params": {"nprobe": 10}},  # 검색 파라미터
        limit=top_k,                          # 반환할 결과 수
        output_fields=[                       # 함께 가져올 메타 필드 목록
            "id", "name", "description", "image_url", "image_width", "image_height",
            "owner_id", "owner_name", "followers", "track_summary", "tag_emotion"
        ]
    )

    # Milvus는 결과를 [[Hit, Hit, ...]] 형태로 반환하므로 첫 묶음만 사용
    return results[0]