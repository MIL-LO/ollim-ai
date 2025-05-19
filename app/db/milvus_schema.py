from pymilvus import Collection
from pymilvus import CollectionSchema
from pymilvus import DataType
from pymilvus import FieldSchema
from pymilvus import connections
from pymilvus import utility


def define_playlist_collection():
    connections.connect("default", host="milvus", port="19530")

    if utility.has_collection("spotify_playlists"):
        print("✅ 이미 'spotify_playlists' 컬렉션이 존재합니다.")
        return

    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
        FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=300),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1000),
        FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="image_width", dtype=DataType.INT64),
        FieldSchema(name="image_height", dtype=DataType.INT64),
        FieldSchema(name="owner_id", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="owner_name", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="followers", dtype=DataType.INT64),
        FieldSchema(name="track_summary", dtype=DataType.VARCHAR, max_length=3000),
        FieldSchema(name="tag_emotion", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]

    schema = CollectionSchema(fields, description="Spotify Playlist Collection with emotion tags")
    collection = Collection(name="spotify_playlists", schema=schema)

    collection.create_index(
        field_name="vector",
        index_params={"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
    )

    collection.load()
    print("✅ 'spotify_playlists' 컬렉션이 생성 및 로드되었습니다.")