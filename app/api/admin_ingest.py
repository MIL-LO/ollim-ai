from fastapi import APIRouter, Query
from typing import List
import json
import os

from app.services.spotify_playlist_fetcher import (
    fetch_playlists_by_genre as fetch_playlists_by_keyword,
    fetch_playlist_details,
)
from app.db.insert_playlist import prepare_insert_data, insert_to_milvus
from app.db.milvus_schema import define_playlist_collection

router = APIRouter()


@router.get("/admin/fetch-and-insert")
def fetch_and_insert_playlists(keywords: List[str] = Query(..., description="수집할 키워드 목록")):
    """
    🔧 Spotify에서 플레이리스트를 수집하고 Milvus에 삽입하는 관리자용 API (GET 요청)
    """
    # 0. Milvus 컬렉션이 없으면 생성
    define_playlist_collection()

    # 1. JSON 데이터 생성
    flattened_data = []

    for kw in keywords:
        playlists = fetch_playlists_by_keyword(kw, limit=10)
        for pl in playlists:
            try:
                detail = fetch_playlist_details(pl["id"])
                track_names = [t["track"]["name"] for t in detail.get("tracks", []) if "track" in t]
                flattened_data.append({
                    "id": detail["id"],
                    "name": detail.get("name", ""),
                    "description": detail.get("description", ""),
                    "image_url": detail.get("image_url", ""),
                    "image_width": detail.get("image_width", 0),
                    "image_height": detail.get("image_height", 0),
                    "owner_id": detail.get("owner_id", ""),
                    "owner_name": detail.get("owner_name", ""),
                    "followers": detail.get("followers", 0),
                    "track_summary": ", ".join(track_names)
                })
            except Exception as e:
                print(f"[ERROR] '{pl.get('name', '')}' 처리 실패: {e}")

    # 2. JSON 저장
    os.makedirs("data", exist_ok=True)
    with open("data/cleaned_playlists.json", "w", encoding="utf-8") as f:
        json.dump(flattened_data, f, ensure_ascii=False, indent=2)

    # 3. Milvus에 삽입
    insert_data = prepare_insert_data(flattened_data)
    insert_to_milvus(insert_data)

    return {"inserted_count": len(flattened_data)}