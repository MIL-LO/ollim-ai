import json
from app.services.spotify_playlist_fetcher import fetch_playlists_by_keyword, fetch_playlist_details

keywords = ["슬픔", "기쁨", "이별", "편안함", "사랑"]
flattened_data = []

for kw in keywords:
    print(f"📚 키워드 '{kw}' 검색 중...")
    playlists = fetch_playlists_by_keyword(kw, limit=10)
    for pl in playlists:
        if pl:
            try:
                detail = fetch_playlist_details(pl["id"])

                # flattening
                track_names = []
                for t in detail.get("tracks", []):
                    try:
                        track_names.append(t["track"]["name"])
                    except (KeyError, TypeError):
                        continue

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
                print(f"⚠️ {pl.get('name')} 실패: {e}")

# 저장
with open("data/cleaned_playlists.json", "w", encoding="utf-8") as f:
    json.dump(flattened_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 총 {len(flattened_data)}개의 플레이리스트가 저장되었습니다.")